"""symkan 分阶段训练与剪枝调度。

该模块实现符号化前的阶段训练入口，包括验证集切分、自适应剪枝阈值、
阶段级早停和快照选模逻辑。
"""

import copy
import time
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import torch

from kan import KAN

from symkan.core import get_device, get_n_edge, model_acc_ds, safe_fit
from symkan.core.runtime import default_batch_size, resolve_device
from symkan.io import clone_model
from symkan.pruning import safe_attribute


def sym_readiness_score(acc, n_edges, sym_target_edges, acc_weight: float = 0.4):
    """计算符号化就绪评分。

    Args:
        acc: 当前模型精度。
        n_edges: 当前边数。
        sym_target_edges: 符号化期望边数。
        acc_weight: 精度权重；稀疏度权重为 ``1 - acc_weight``。

    Returns:
        float: 综合评分，分数越高表示越适合作为符号化入口。
    """
    if n_edges <= sym_target_edges:
        prune_burden = 0.0
    else:
        prune_burden = (n_edges - sym_target_edges) / n_edges
    sparsity_score = 1.0 - prune_burden
    return acc_weight * acc + (1.0 - acc_weight) * sparsity_score


def _has_split(dataset, split: str) -> bool:
    input_key = f"{split}_input"
    label_key = f"{split}_label"
    return input_key in dataset and label_key in dataset and dataset[input_key] is not None and dataset[label_key] is not None


def _valid_edge_count(value) -> bool:
    try:
        return bool(np.isfinite(float(value)))
    except Exception:
        return False


def _create_validation_split(dataset, ratio: float, seed: Optional[int], min_val_samples: int = 10):
    """在现有 dataset 上以复制字典的方式创建验证集切分。

    Args:
        dataset: 原始数据集字典。
        ratio: 验证集比例。
        seed: 随机种子。
        min_val_samples: 验证集最少样本数。

    Returns:
        dict: 包含训练集和验证集的新数据字典。
    """
    if _has_split(dataset, "val") or ratio <= 0:
        return dataset

    train_input = dataset["train_input"]
    train_label = dataset["train_label"]
    n_total = int(train_input.shape[0])
    if n_total <= 1:
        warnings.warn(
            f"训练样本过少 (n_total={n_total})，禁用验证集。",
            category=UserWarning,
            stacklevel=2,
        )
        merged = dict(dataset)
        merged["val_input"] = None
        merged["val_label"] = None
        return merged

    n_val = int(n_total * float(ratio))
    effective_ratio = float(ratio)
    if n_val < min_val_samples:
        adjusted_ratio = min(float(min_val_samples) / float(n_total), 0.3)
        if adjusted_ratio > effective_ratio:
            warnings.warn(
                f"validation_ratio 从 {effective_ratio:.3f} 调整为 {adjusted_ratio:.3f}，"
                f"以保证至少 {min_val_samples} 个验证样本。",
                category=UserWarning,
                stacklevel=2,
            )
            effective_ratio = adjusted_ratio
            n_val = int(n_total * effective_ratio)

    if n_val < min_val_samples:
        warnings.warn(
            f"训练样本不足以稳定切分验证集 (n_total={n_total})，已禁用验证集。",
            category=UserWarning,
            stacklevel=2,
        )
        merged = dict(dataset)
        merged["val_input"] = None
        merged["val_label"] = None
        return merged

    rng = np.random.default_rng(seed)
    perm = rng.permutation(n_total)
    device = train_input.device if torch.is_tensor(train_input) else None
    val_idx = torch.as_tensor(perm[:n_val], dtype=torch.long, device=device)
    train_idx = torch.as_tensor(perm[n_val:], dtype=torch.long, device=device)

    merged = dict(dataset)
    merged["train_input"] = train_input[train_idx]
    merged["train_label"] = train_label[train_idx]
    merged["val_input"] = train_input[val_idx]
    merged["val_label"] = train_label[val_idx]
    return merged


def _safe_eval_acc(model, dataset, preferred_split: str = "val"):
    """优先验证集，不可用时回退到训练集。

    Args:
        model: 待评估模型。
        dataset: 数据集字典。
        preferred_split: 优先尝试的数据划分。

    Returns:
        tuple[float, str]: 精度和实际使用的划分名称。
    """
    if preferred_split == "val" and _has_split(dataset, "val"):
        return model_acc_ds(model, dataset, split="val"), "val"
    if preferred_split != "train" and _has_split(dataset, preferred_split):
        return model_acc_ds(model, dataset, split=preferred_split), preferred_split
    return model_acc_ds(model, dataset, split="train"), "train"


def _safe_attribute_for_prune(model, dataset):
    try:
        safe_attribute(model, dataset)
        return None
    except Exception as exc:
        if hasattr(model, "width_in"):
            size = int(model.width_in[0])
            device = next(model.parameters()).device
            model.feature_score = torch.ones(size, dtype=torch.float32, device=device)
        return str(exc)


def _compute_adaptive_lamb(
    base_lamb: float,
    current_edges,
    initial_edges,
    target_edges: int,
    min_lamb_ratio: float = 0.3,
    max_lamb_ratio: float = 1.5,
):
    if not (_valid_edge_count(current_edges) and _valid_edge_count(initial_edges)):
        return float(base_lamb)
    current_edges = float(current_edges)
    initial_edges = float(initial_edges)
    target_edges = float(target_edges)
    denom = max(initial_edges - target_edges, 1.0)
    if current_edges <= target_edges:
        return float(base_lamb) * 0.2
    sparsity_ratio = np.clip((initial_edges - current_edges) / denom, 0.0, 1.0)
    if sparsity_ratio < 0.3:
        return float(base_lamb) * max_lamb_ratio
    if sparsity_ratio < 0.7:
        return float(base_lamb)
    return float(base_lamb) * min_lamb_ratio


def _compute_adaptive_ft_steps(
    base_steps: int,
    current_edges,
    initial_edges,
    target_edges: int,
    min_ratio: float = 0.3,
):
    if base_steps <= 0:
        return 0
    if not (_valid_edge_count(current_edges) and _valid_edge_count(initial_edges)):
        return int(base_steps)
    current_edges = float(current_edges)
    initial_edges = float(initial_edges)
    target_edges = float(target_edges)
    denom = max(initial_edges - target_edges, 1.0)
    if current_edges <= target_edges:
        return max(1, int(base_steps // 2))
    sparsity_ratio = np.clip((initial_edges - current_edges) / denom, 0.0, 1.0)
    steps_ratio = max(min_ratio, 1.0 - 0.7 * sparsity_ratio)
    return max(1, int(base_steps * steps_ratio))


@dataclass
class AdaptiveThresholdController:
    """剪枝阈值自适应控制器。

    根据最近剪枝收益和成功次数动态调整下一轮阈值。
    """

    base_step: float = 0.005
    min_threshold: float = 0.001
    max_threshold: float = 0.1
    success_boost: float = 0.5
    failure_penalty: float = 0.3
    current_threshold: float = 0.005
    max_history: int = 10
    success_count: int = 0
    failure_count: int = 0
    total_prunes: int = 0
    total_successes: int = 0
    history: List[Dict[str, float]] = field(default_factory=list)

    def update(self, success: bool, edges_removed: int):
        self.total_prunes += 1
        entry = {
            "threshold": float(self.current_threshold),
            "success": float(bool(success)),
            "edges_removed": float(max(0, int(edges_removed))),
            "stage": float(self.total_prunes),
        }
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        effective_success = bool(success) and int(edges_removed) > 0
        if effective_success:
            self.success_count += 1
            self.failure_count = 0
            self.total_successes += 1
            boost = 1.0 + min(3.0, self.success_count * self.success_boost)
            new_threshold = self.current_threshold + self.base_step * boost
        else:
            self.failure_count += 1
            self.success_count = 0
            penalty = 0.3 * (1.0 + min(2.0, self.failure_count * self.failure_penalty))
            new_threshold = self.current_threshold - self.base_step * penalty

        self.current_threshold = float(np.clip(new_threshold, self.min_threshold, self.max_threshold))
        return self.current_threshold

    def should_continue(self, min_gain_threshold: int = 3):
        if len(self.history) < 3:
            return True
        recent = self.history[-3:]
        avg_gain = sum(item["edges_removed"] for item in recent) / float(len(recent))
        if avg_gain < float(min_gain_threshold):
            return False
        if self.current_threshold > self.max_threshold * 0.8:
            return False
        return True


def _attempt_prune_with_validation(
    model,
    dataset,
    threshold: float,
    current_lr: float,
    current_lamb: float,
    batch_size: int,
    prune_acc_drop_tol: float = 0.03,
    post_prune_ft_steps: int = 40,
    use_disk_clone: bool = False,
    clone_ckpt_path: str = "_safe_copy_temp",
):
    """用验证反馈执行单次剪枝尝试。

    Args:
        model: 当前阶段模型。
        dataset: 数据集字典。
        threshold: 本轮剪枝阈值。
        current_lr: 当前学习率。
        current_lamb: 当前正则强度。
        batch_size: 批大小。
        prune_acc_drop_tol: 允许的精度回落阈值。
        post_prune_ft_steps: 剪枝后恢复微调步数。
        use_disk_clone: 是否使用磁盘克隆回滚快照。
        clone_ckpt_path: 磁盘克隆临时路径前缀。

    Returns:
        dict: 包含回滚模型、是否成功、边数收益和评估信息的记录。
    """
    snapshot = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
    eval_before, eval_split = _safe_eval_acc(model, dataset, preferred_split="val")
    attribute_warning = _safe_attribute_for_prune(model, dataset)

    try:
        edges_before = get_n_edge(model)
        model.prune_edge(threshold=threshold)
        edges_after = get_n_edge(model)
        if _valid_edge_count(edges_before) and _valid_edge_count(edges_after):
            edges_removed = max(0, int(round(float(edges_before) - float(edges_after))))
        else:
            edges_removed = 0

        # 先做一次短恢复，尽快判断这轮剪枝是否值得保留，避免把大步数微调浪费在坏剪枝上。
        quick_ft_steps = min(int(post_prune_ft_steps), 20) if post_prune_ft_steps > 0 else 0
        if edges_removed > 0 and quick_ft_steps > 0:
            safe_fit(
                model,
                dataset,
                opt="Adam",
                steps=quick_ft_steps,
                lr=current_lr * 0.5,
                lamb=current_lamb * 0.1,
                batch=batch_size,
                update_grid=False,
                singularity_avoiding=True,
                log=max(1, quick_ft_steps // 5),
            )

        eval_after, _ = _safe_eval_acc(model, dataset, preferred_split=eval_split)
        eval_drop = float(eval_before - eval_after)
        success = eval_drop <= prune_acc_drop_tol and edges_removed > 0
        if success:
            remain_ft_steps = max(0, int(post_prune_ft_steps) - quick_ft_steps)
            if remain_ft_steps > 0:
                safe_fit(
                    model,
                    dataset,
                    opt="Adam",
                    steps=remain_ft_steps,
                    lr=current_lr * 0.5,
                    lamb=current_lamb * 0.1,
                    batch=batch_size,
                    update_grid=False,
                    singularity_avoiding=True,
                    log=max(1, remain_ft_steps // 5),
                )
            return {
                "model": model,
                "success": True,
                "edges_removed": edges_removed,
                "eval_drop": eval_drop,
                "threshold": float(threshold),
                "eval_split": eval_split,
                "rollback": "",
                "attribute_warning": attribute_warning,
            }

        return {
            "model": snapshot,
            "success": False,
            "edges_removed": 0,
            "eval_drop": eval_drop,
            "threshold": float(threshold),
            "eval_split": eval_split,
            "rollback": f"prune_acc_drop({eval_before:.4f}->{eval_after:.4f})",
            "attribute_warning": attribute_warning,
        }
    except Exception as exc:
        return {
            "model": snapshot,
            "success": False,
            "edges_removed": 0,
            "eval_drop": np.nan,
            "threshold": float(threshold),
            "eval_split": eval_split,
            "rollback": f"prune_error: {exc}",
            "attribute_warning": attribute_warning,
        }


def stagewise_train(
    dataset,
    width,
    grid=5,
    k=3,
    seed=123,
    lamb_schedule=(0.0, 1e-4, 3e-4),
    lr_schedule=(0.02, 0.012, 0.006),
    steps_per_stage=70,
    batch_size=None,
    prune_start_stage=1,
    target_edges=100,
    prune_edge_threshold_init=0.005,
    prune_edge_threshold_step=0.005,
    prune_acc_drop_tol=0.03,
    post_prune_ft_steps=40,
    sym_target_edges=50,
    acc_weight=0.4,
    keep_topk_models=0,
    keep_full_snapshots=False,
    use_disk_clone=False,
    clone_ckpt_path="_safe_copy_temp",
    use_validation=False,
    validation_ratio=0.0,
    validation_seed=None,
    validation_min_samples=10,
    adaptive_threshold=False,
    threshold_base_step=0.005,
    threshold_min=0.001,
    threshold_max=0.1,
    success_boost=0.5,
    failure_penalty=0.3,
    min_gain_threshold=3,
    max_prune_attempts=20,
    adaptive_lamb=False,
    min_lamb_ratio=0.3,
    max_lamb_ratio=1.5,
    adaptive_ft=False,
    min_ft_ratio=0.3,
    stage_early_stop=False,
    stage_early_stop_patience=2,
    stage_early_stop_min_acc_gain=0.002,
    stage_early_stop_edge_buffer=0,
    verbose=True,
):
    """分阶段训练并自动选择最优快照。

    该流程在每个阶段执行拟合，并在满足条件时进行渐进式剪枝、短微调与回滚保护，
    最终依据 ``sym_readiness_score`` 从多阶段快照中选出符号化入口模型。

    Args:
        dataset: 由 ``build_dataset`` 构建的数据字典。
        width: KAN 网络宽度配置，例如 ``[in_dim, hidden_dim, out_dim]``。
        grid: KAN spline grid 数。
        k: KAN spline 阶数。
        seed: 随机种子。
        lamb_schedule: 分阶段稀疏正则序列。
        lr_schedule: 分阶段学习率序列。
        steps_per_stage: 每阶段训练步数。
        batch_size: 批大小；为空时自动使用默认值。
        prune_start_stage: 从该阶段开始允许剪枝。
        target_edges: 阶段训练目标边数。
        prune_edge_threshold_init: 剪枝阈值初值。
        prune_edge_threshold_step: 剪枝阈值递增步长。
        prune_acc_drop_tol: 剪枝后允许的精度回落阈值。
        post_prune_ft_steps: 每次剪枝后的恢复微调步数。
        sym_target_edges: 选模时使用的符号化目标边数。
        acc_weight: 选模中精度权重。
        keep_topk_models: 是否保留 Top-K 完整模型快照。
        keep_full_snapshots: 是否保留每阶段完整模型对象。
        use_disk_clone: 是否强制使用磁盘克隆。
        clone_ckpt_path: 磁盘克隆临时路径前缀。
        use_validation: 是否启用验证集引导剪枝；默认关闭以保持旧行为。
        validation_ratio: 训练集切出验证集比例；已有验证集时忽略。
        validation_seed: 验证集切分随机种子。
        validation_min_samples: 验证集最少样本数。
        adaptive_threshold: 是否启用自适应剪枝阈值。
        threshold_base_step: 自适应阈值基础步长。
        threshold_min: 自适应阈值下界。
        threshold_max: 自适应阈值上界。
        success_boost: 连续成功时的阈值增益系数。
        failure_penalty: 连续失败时的阈值惩罚系数。
        min_gain_threshold: 最近剪枝平均收益低于该值时提前停止。
        max_prune_attempts: 单阶段最多剪枝尝试次数。
        adaptive_lamb: 是否根据稀疏进度调整 lamb。
        min_lamb_ratio: lamb 下界倍数。
        max_lamb_ratio: lamb 上界倍数。
        adaptive_ft: 是否按稀疏进度缩放剪枝后微调步数。
        min_ft_ratio: 微调步数下界比例。
        stage_early_stop: 是否启用阶段级早停。
        stage_early_stop_patience: 达到目标后连续低收益阶段耐心值。
        stage_early_stop_min_acc_gain: 阶段级最小有效精度提升阈值。
        stage_early_stop_edge_buffer: 早停判定时允许的目标边数缓冲。
        verbose: 是否打印详细日志。

    Returns:
        tuple: ``(best_model, result_dict)``，分别是最优模型与阶段训练结果。
    """
    if batch_size is None:
        batch_size = default_batch_size()

    if use_validation:
        dataset = _create_validation_split(
            dataset,
            ratio=float(validation_ratio),
            seed=validation_seed,
            min_val_samples=int(validation_min_samples),
        )

    model_device = str(resolve_device(get_device()))

    model = KAN(
        width=width,
        grid=grid,
        k=k,
        seed=seed,
        auto_save=False,
        symbolic_enabled=True,
        save_act=True,
        device=model_device,
    )
    all_train_loss, all_test_loss = [], []
    stage_logs = []
    stage_snapshots = []
    stage_state_dicts = []
    topk_models = []
    stage_timings = []
    stage_train_total_seconds = 0.0
    stage_prune_total_seconds = 0.0
    stagewise_t0 = time.perf_counter()

    cur_prune_th = prune_edge_threshold_init
    max_acc_seen = 0.0
    initial_edges = get_n_edge(model)
    controller = None
    stage_stall_count = 0
    stage_early_stopped = False
    stage_early_stop_reason = ""
    if adaptive_threshold:
        controller = AdaptiveThresholdController(
            base_step=threshold_base_step,
            min_threshold=threshold_min,
            max_threshold=threshold_max,
            success_boost=success_boost,
            failure_penalty=failure_penalty,
            current_threshold=prune_edge_threshold_init,
        )

    for si, lamb in enumerate(lamb_schedule):
        stage_t0 = time.perf_counter()
        lr = float(lr_schedule[min(si, len(lr_schedule) - 1)])
        acc_before = model_acc_ds(model, dataset)
        edge_before = get_n_edge(model)
        rollback = ""
        train_seconds = 0.0
        prune_seconds = 0.0
        stage_lamb = float(lamb)
        if adaptive_lamb:
            stage_lamb = _compute_adaptive_lamb(
                lamb,
                edge_before,
                initial_edges,
                target_edges,
                min_lamb_ratio=min_lamb_ratio,
                max_lamb_ratio=max_lamb_ratio,
            )
        prune_attempts = []

        try:
            fit_t0 = time.perf_counter()
            res = safe_fit(
                model,
                dataset,
                opt="Adam",
                steps=steps_per_stage,
                lr=lr,
                lamb=stage_lamb,
                batch=batch_size,
                update_grid=(si == 0),
                singularity_avoiding=True,
                log=max(1, steps_per_stage // 10),
            )
            train_seconds = float(time.perf_counter() - fit_t0)
            stage_train_total_seconds += train_seconds
            all_train_loss.extend(list(res.get("train_loss", [])))
            all_test_loss.extend(list(res.get("test_loss", [])))
        except Exception as e:
            rollback = f"fit_error: {e}"
            if verbose:
                print(f"  [stage {si}] fit 异常: {e}")

        prune_accepted = False
        if si >= prune_start_stage and get_n_edge(model) > target_edges and not rollback:
            prune_t0 = time.perf_counter()
            if adaptive_threshold and controller is not None:
                attempt_idx = 0
                while attempt_idx < max_prune_attempts and get_n_edge(model) > target_edges:
                    if attempt_idx > 0 and not controller.should_continue(min_gain_threshold=min_gain_threshold):
                        rollback = rollback or "adaptive_stop: low prune gain"
                        break
                    current_edges = get_n_edge(model)
                    current_lamb = stage_lamb
                    if adaptive_lamb:
                        current_lamb = _compute_adaptive_lamb(
                            lamb,
                            current_edges,
                            initial_edges,
                            target_edges,
                            min_lamb_ratio=min_lamb_ratio,
                            max_lamb_ratio=max_lamb_ratio,
                        )
                    current_ft_steps = int(post_prune_ft_steps)
                    if adaptive_ft:
                        current_ft_steps = _compute_adaptive_ft_steps(
                            post_prune_ft_steps,
                            current_edges,
                            initial_edges,
                            target_edges,
                            min_ratio=min_ft_ratio,
                        )

                    attempt = _attempt_prune_with_validation(
                        model,
                        dataset,
                        threshold=controller.current_threshold,
                        current_lr=lr,
                        current_lamb=current_lamb,
                        batch_size=batch_size,
                        prune_acc_drop_tol=prune_acc_drop_tol,
                        post_prune_ft_steps=current_ft_steps,
                        use_disk_clone=use_disk_clone,
                        clone_ckpt_path=clone_ckpt_path,
                    )
                    model = attempt["model"]
                    # 控制器始终基于最近一次尝试更新阈值，即使回滚了模型也一样，
                    # 因为失败本身就是下一轮调阈的信号。
                    controller.update(attempt["success"], attempt["edges_removed"])
                    cur_prune_th = controller.current_threshold
                    prune_accepted = prune_accepted or bool(attempt["success"])
                    if attempt["rollback"]:
                        rollback = attempt["rollback"]
                    prune_attempts.append(
                        {
                            "attempt": attempt_idx,
                            "threshold": float(attempt["threshold"]),
                            "success": bool(attempt["success"]),
                            "edges_removed": int(attempt["edges_removed"]),
                            "eval_drop": float(attempt["eval_drop"]) if np.isfinite(attempt["eval_drop"]) else np.nan,
                            "eval_split": attempt["eval_split"],
                            "attribute_warning": attempt["attribute_warning"],
                            "threshold_next": float(cur_prune_th),
                        }
                    )
                    attempt_idx += 1
                    if not attempt["success"] and int(attempt["edges_removed"]) == 0 and not controller.should_continue(min_gain_threshold=min_gain_threshold):
                        break
            else:
                snap = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
                try:
                    threshold_used = float(cur_prune_th)
                    attr_warning = _safe_attribute_for_prune(model, dataset)
                    edges_before_prune = get_n_edge(model)
                    model.prune_edge(threshold=cur_prune_th)

                    safe_fit(
                        model,
                        dataset,
                        opt="Adam",
                        steps=post_prune_ft_steps,
                        lr=lr * 0.5,
                        lamb=stage_lamb * 0.1,
                        batch=batch_size,
                        update_grid=False,
                        singularity_avoiding=True,
                        log=max(1, post_prune_ft_steps // 5),
                    )
                    acc_after_prune = model_acc_ds(model, dataset)

                    if acc_after_prune + prune_acc_drop_tol >= acc_before:
                        prune_accepted = True
                        cur_prune_th += prune_edge_threshold_step
                    else:
                        rollback = f"prune_acc_drop({acc_before:.4f}->{acc_after_prune:.4f})"
                        model = snap
                        cur_prune_th += prune_edge_threshold_step * 0.3

                    prune_attempts.append(
                        {
                            "attempt": 0,
                            "threshold": threshold_used,
                            "success": bool(prune_accepted),
                            "edges_removed": max(0, int(edges_before_prune - get_n_edge(model))) if _valid_edge_count(edges_before_prune) and _valid_edge_count(get_n_edge(model)) else 0,
                            "eval_drop": float(acc_before - acc_after_prune),
                            "eval_split": "test",
                            "attribute_warning": attr_warning,
                            "threshold_next": float(cur_prune_th),
                        }
                    )
                except Exception as e:
                    rollback = f"prune_error: {e}"
                    model = snap
            prune_seconds = float(time.perf_counter() - prune_t0)
            stage_prune_total_seconds += prune_seconds

        acc_after = model_acc_ds(model, dataset)
        edge_after = get_n_edge(model)
        max_acc_seen = max(max_acc_seen, acc_after)

        score = sym_readiness_score(acc_after, edge_after, sym_target_edges, acc_weight)
        state_dict_cpu = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        stage_state_dicts.append({"stage": si, "state_dict": state_dict_cpu})

        snapshot = {
            "stage": si,
            "acc": float(acc_after),
            "n_edges": edge_after,
            "score": float(score),
        }
        if keep_full_snapshots:
            snapshot["model"] = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
        else:
            snapshot["model"] = None
        stage_snapshots.append(snapshot)

        if keep_topk_models and keep_topk_models > 0:
            topk_models.append(
                {
                    "stage": si,
                    "acc": float(acc_after),
                    "n_edges": edge_after,
                    "score": float(score),
                    "model": clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path),
                }
            )
            topk_models.sort(key=lambda s: s["score"], reverse=True)
            if len(topk_models) > keep_topk_models:
                topk_models = topk_models[:keep_topk_models]

        stage_logs.append(
            {
                "stage": si,
                "lamb": float(lamb),
                "effective_lamb": float(stage_lamb),
                "lr": lr,
                "acc_before": float(acc_before),
                "acc_after": float(acc_after),
                "edges_before": edge_before,
                "edges_after": edge_after,
                "prune_accepted": prune_accepted,
                "prune_attempts": prune_attempts,
                "prune_attempt_count": len(prune_attempts),
                "rollback": rollback,
                "prune_th": float(cur_prune_th),
                "sym_score": float(score),
                "train_seconds": float(train_seconds),
                "prune_seconds": float(prune_seconds),
                "stage_seconds": float(time.perf_counter() - stage_t0),
            }
        )
        stage_timings.append(
            {
                "stage": int(si),
                "train_seconds": float(train_seconds),
                "prune_seconds": float(prune_seconds),
                "stage_seconds": float(time.perf_counter() - stage_t0),
            }
        )
        if verbose:
            prune_suffix = f" attempts={len(prune_attempts)}" if prune_attempts else ""
            print(
                f"[stage {si}] λ={lamb:.1e} lr={lr:.4f}  "
                f"acc {acc_before:.4f}→{acc_after:.4f}  "
                f"edges {edge_before}→{edge_after}  "
                f"score={score:.3f}  "
                f"prune={'✓' if prune_accepted else '✗'}{prune_suffix}  "
                f"{'⚠ ' + rollback if rollback else ''}"
            )

        if stage_early_stop and si >= prune_start_stage:
            close_to_target = (
                _valid_edge_count(edge_after)
                and float(edge_after) <= float(target_edges + max(0, int(stage_early_stop_edge_buffer)))
            )
            stage_gain = float(acc_after - acc_before)
            if close_to_target and stage_gain < float(stage_early_stop_min_acc_gain):
                stage_stall_count += 1
            else:
                stage_stall_count = 0

            if stage_stall_count >= max(1, int(stage_early_stop_patience)):
                stage_early_stopped = True
                stage_early_stop_reason = (
                    f"stage_early_stop: close_to_target={close_to_target}, "
                    f"gain={stage_gain:.6f} < {float(stage_early_stop_min_acc_gain):.6f}, "
                    f"stall={stage_stall_count}"
                )
                if verbose:
                    print(f"[stage {si}] {stage_early_stop_reason}")
                break

    final_finetune_seconds = 0.0
    try:
        final_fit_t0 = time.perf_counter()
        final_res = safe_fit(
            model,
            dataset,
            opt="Adam",
            steps=60,
            lr=0.005,
            lamb=0.0,
            batch=batch_size,
            update_grid=False,
            singularity_avoiding=True,
            log=10,
        )
        final_finetune_seconds = float(time.perf_counter() - final_fit_t0)
        all_train_loss.extend(list(final_res.get("train_loss", [])))
        all_test_loss.extend(list(final_res.get("test_loss", [])))
    except Exception:
        pass

    final_acc = model_acc_ds(model, dataset)
    final_edges = get_n_edge(model)
    final_score = sym_readiness_score(final_acc, final_edges, sym_target_edges, acc_weight)
    max_acc_seen = max(max_acc_seen, final_acc)

    final_state_dict_cpu = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    stage_state_dicts.append({"stage": "final", "state_dict": final_state_dict_cpu})

    final_snapshot = {
        "stage": "final",
        "acc": float(final_acc),
        "n_edges": final_edges,
        "score": float(final_score),
    }
    if keep_full_snapshots:
        final_snapshot["model"] = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
    else:
        final_snapshot["model"] = None
    stage_snapshots.append(final_snapshot)

    if keep_topk_models and keep_topk_models > 0:
        topk_models.append(
            {
                "stage": "final",
                "acc": float(final_acc),
                "n_edges": final_edges,
                "score": float(final_score),
                "model": clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path),
            }
        )
        topk_models.sort(key=lambda s: s["score"], reverse=True)
        if len(topk_models) > keep_topk_models:
            topk_models = topk_models[:keep_topk_models]

    acc_floor = max_acc_seen * 0.65
    candidates = [s for s in stage_snapshots if s["acc"] >= acc_floor]
    if not candidates:
        candidates = stage_snapshots

    # 先按精度过滤，再按 readiness score 选模，避免为了稀疏度牺牲过多精度。
    candidates.sort(key=lambda s: s["score"], reverse=True)
    best_snap = candidates[0]

    selected_state = None
    for item in reversed(stage_state_dicts):
        if item["stage"] == best_snap["stage"]:
            selected_state = item["state_dict"]
            break
    if selected_state is None:
        selected_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}

    best_model = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
    best_model.load_state_dict(selected_state)

    if verbose:
        print(f"\n{'─' * 50}")
        print(f"模型选择（sym_readiness_score, acc_weight={acc_weight}）:")
        print(f"  精度下限: {acc_floor:.4f} (max_acc={max_acc_seen:.4f} × 0.65)")
        print(f"  候选数量: {len(candidates)}/{len(stage_snapshots)}")
        print(
            f"  ▸ 选中 stage={best_snap['stage']}, "
            f"acc={best_snap['acc']:.4f}, "
            f"edges={best_snap['n_edges']}, "
            f"score={best_snap['score']:.3f}"
        )

    result = {
        "train_loss": all_train_loss,
        "test_loss": all_test_loss,
        "stage_logs": stage_logs,
        "best_acc": float(best_snap["acc"]),
        "selected_stage": best_snap["stage"],
        "selected_edges": best_snap["n_edges"],
        "selected_score": float(best_snap["score"]),
        "best_state_dict": copy.deepcopy(selected_state),
        "stage_snapshots": stage_snapshots,
        "stage_early_stopped": bool(stage_early_stopped),
        "stage_early_stop_reason": stage_early_stop_reason,
        "stage_timings": stage_timings,
        "stage_train_total_seconds": float(stage_train_total_seconds),
        "stage_prune_total_seconds": float(stage_prune_total_seconds),
        "final_finetune_seconds": float(final_finetune_seconds),
        "stage_total_seconds": float(time.perf_counter() - stagewise_t0),
    }
    if keep_topk_models and keep_topk_models > 0:
        result["topk_models"] = topk_models

    return best_model, result


def stagewise_train_report(dataset, width, **kwargs):
    """返回 ``stagewise_train`` 的结构化报告版本。

    Args:
        dataset: 数据集字典。
        width: KAN 网络宽度配置。
        **kwargs: 传递给 ``stagewise_train`` 的其余参数。

    Returns:
        tuple: ``(best_model, StagewiseResult)``。
    """
    from symkan.core.types import StagewiseResult

    best_model, result = stagewise_train(dataset, width, **kwargs)
    sr = StagewiseResult(
        best_model=best_model,
        train_loss=result.get("train_loss", []),
        test_loss=result.get("test_loss", []),
        stage_logs=result.get("stage_logs", []),
        best_acc=result.get("best_acc", 0.0),
        selected_stage=result.get("selected_stage", 0),
        selected_edges=result.get("selected_edges", 0),
        selected_score=result.get("selected_score", 0.0),
        best_state_dict=result.get("best_state_dict"),
        stage_snapshots=result.get("stage_snapshots", []),
        topk_models=result.get("topk_models"),
    )
    return best_model, sr
