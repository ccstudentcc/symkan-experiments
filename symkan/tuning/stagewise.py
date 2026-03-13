import copy

import numpy as np

from kan import KAN

from symkan.core import get_device, get_n_edge, model_acc_ds, safe_fit
from symkan.core.runtime import default_batch_size, resolve_device
from symkan.io import clone_model
from symkan.pruning import safe_attribute


def sym_readiness_score(acc, n_edges, sym_target_edges, acc_weight: float = 0.4):
    """@brief 计算符号化就绪评分（精度与稀疏度折中）。

    @param acc 当前模型精度。
    @param n_edges 当前边数。
    @param sym_target_edges 符号化期望边数。
    @param acc_weight 精度权重；稀疏度权重为 `1-acc_weight`。
    @return float 综合评分，分数越高表示越适合作为符号化入口。
    """
    if n_edges <= sym_target_edges:
        prune_burden = 0.0
    else:
        prune_burden = (n_edges - sym_target_edges) / n_edges
    sparsity_score = 1.0 - prune_burden
    return acc_weight * acc + (1.0 - acc_weight) * sparsity_score


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
    verbose=True,
):
    """@brief 分阶段训练并自动选择最优快照。

    本流程在每个阶段执行拟合，并在满足条件时进行渐进式剪枝、短微调与回滚保护，
    最终依据 `sym_readiness_score` 从多阶段快照中选出符号化入口模型。

    @param dataset 由 `build_dataset` 构建的数据字典。
    @param width KAN 网络宽度配置，如 `[in_dim, hidden_dim, out_dim]`。
    @param grid KAN spline grid 数。
    @param k KAN spline 阶数。
    @param seed 随机种子。
    @param lamb_schedule 分阶段稀疏正则序列。
    @param lr_schedule 分阶段学习率序列。
    @param steps_per_stage 每阶段训练步数。
    @param batch_size 批大小；为空时自动使用默认值。
    @param prune_start_stage 从该阶段开始允许剪枝。
    @param target_edges 阶段训练目标边数。
    @param prune_edge_threshold_init 剪枝阈值初值。
    @param prune_edge_threshold_step 剪枝阈值递增步长。
    @param prune_acc_drop_tol 剪枝后允许的精度回落阈值。
    @param post_prune_ft_steps 每次剪枝后的恢复微调步数。
    @param sym_target_edges 选模时使用的符号化目标边数。
    @param acc_weight 选模中精度权重。
    @param keep_topk_models 是否保留 Top-K 完整模型快照。
    @param keep_full_snapshots 是否保留每阶段完整模型对象。
    @param use_disk_clone 是否强制使用磁盘克隆。
    @param clone_ckpt_path 磁盘克隆临时路径前缀。
    @param verbose 是否打印详细日志。
    @return tuple(best_model, result_dict) 最优模型与阶段训练结果。
    """
    if batch_size is None:
        batch_size = default_batch_size()

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

    cur_prune_th = prune_edge_threshold_init
    max_acc_seen = 0.0

    for si, lamb in enumerate(lamb_schedule):
        lr = float(lr_schedule[min(si, len(lr_schedule) - 1)])
        acc_before = model_acc_ds(model, dataset)
        edge_before = get_n_edge(model)
        rollback = ""

        try:
            res = safe_fit(
                model,
                dataset,
                opt="Adam",
                steps=steps_per_stage,
                lr=lr,
                lamb=lamb,
                batch=batch_size,
                update_grid=(si == 0),
                singularity_avoiding=True,
                log=max(1, steps_per_stage // 10),
            )
            all_train_loss.extend(list(res.get("train_loss", [])))
            all_test_loss.extend(list(res.get("test_loss", [])))
        except Exception as e:
            rollback = f"fit_error: {e}"
            if verbose:
                print(f"  [stage {si}] fit 异常: {e}")

        prune_accepted = False
        if si >= prune_start_stage and get_n_edge(model) > target_edges and not rollback:
            snap = clone_model(model, use_disk_clone=use_disk_clone, ckpt_path=clone_ckpt_path)
            try:
                safe_attribute(model, dataset)
                model.prune_edge(threshold=cur_prune_th)

                safe_fit(
                    model,
                    dataset,
                    opt="Adam",
                    steps=post_prune_ft_steps,
                    lr=lr * 0.5,
                    lamb=lamb * 0.1,
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
            except Exception as e:
                rollback = f"prune_error: {e}"
                model = snap

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
                "lamb": lamb,
                "lr": lr,
                "acc_before": float(acc_before),
                "acc_after": float(acc_after),
                "edges_before": edge_before,
                "edges_after": edge_after,
                "prune_accepted": prune_accepted,
                "rollback": rollback,
                "prune_th": float(cur_prune_th),
                "sym_score": float(score),
            }
        )
        if verbose:
            print(
                f"[stage {si}] λ={lamb:.1e} lr={lr:.4f}  "
                f"acc {acc_before:.4f}→{acc_after:.4f}  "
                f"edges {edge_before}→{edge_after}  "
                f"score={score:.3f}  "
                f"prune={'✓' if prune_accepted else '✗'}  "
                f"{'⚠ ' + rollback if rollback else ''}"
            )

    try:
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
    }
    if keep_topk_models and keep_topk_models > 0:
        result["topk_models"] = topk_models

    return best_model, result


def stagewise_train_report(dataset, width, **kwargs):
    """@brief stagewise_train 的结构化报告版本。

    参数与 stagewise_train 完全一致。
    @return tuple(best_model, StagewiseResult) 模型与结构化结果对象。
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
