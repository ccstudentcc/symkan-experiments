"""symkan 训练封装与容错原语。

从原 modeling.py 迁移。提供 safe_fit 及结构化训练报告。
"""

import os
from typing import Optional

from .types import FitReport


def _ensure_model_history_path(model):
    ckpt_path = getattr(model, "ckpt_path", None)
    if not isinstance(ckpt_path, str) or len(ckpt_path) == 0:
        return False

    os.makedirs(ckpt_path, exist_ok=True)
    history_path = os.path.join(ckpt_path, "history.txt")
    if not os.path.exists(history_path):
        with open(history_path, "a", encoding="utf-8"):
            pass
    return True


def safe_fit(
    model,
    dataset,
    opt: str = "Adam",
    steps: int = 50,
    lr: float = 0.01,
    lamb: float = 0,
    lamb_l1: float = 1.0,
    lamb_entropy: float = 0.0,
    batch: int = -1,
    update_grid: bool = False,
    singularity_avoiding: bool = True,
    log: int = 10,
):
    """带自动降级与容错的训练封装。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        opt: 优化器名称，如 ``Adam`` 或 ``LBFGS``。
        steps: 训练步数。
        lr: 学习率。
        lamb: 稀疏正则权重。
        lamb_l1: L1 正则系数。
        lamb_entropy: 熵正则系数。
        batch: 批大小；``-1`` 表示全量。
        update_grid: 是否更新 grid。
        singularity_avoiding: 是否启用奇异点规避。
        log: 日志间隔。

    Returns:
        dict: 训练过程结果字典（失败时返回空字典）。
    """
    kw = dict(
        dataset=dataset,
        opt=opt,
        steps=steps,
        lr=lr,
        lamb=lamb,
        lamb_l1=lamb_l1,
        lamb_entropy=lamb_entropy,
        batch=batch,
        update_grid=update_grid,
        singularity_avoiding=singularity_avoiding,
        log=log,
    )
    if batch == -1:
        kw.pop("batch")

    _ensure_model_history_path(model)

    try:
        return model.fit(**kw)
    except Exception as e:
        if "history.txt" in str(e):
            try:
                _ensure_model_history_path(model)
                return model.fit(**kw)
            except Exception as e_retry:
                e = e_retry
        if update_grid:
            print(f"  [safe_fit] grid update 失败 ({e})，关闭 update_grid 重试")
            kw["update_grid"] = False
            try:
                return model.fit(**kw)
            except Exception as e2:
                print(f"  [safe_fit] 仍失败 ({e2})，跳过")
                return {}
        print(f"  [safe_fit] 训练失败 ({e})，跳过")
        return {}


def safe_fit_report(
    model,
    dataset,
    opt: str = "Adam",
    steps: int = 50,
    lr: float = 0.01,
    lamb: float = 0,
    lamb_l1: float = 1.0,
    lamb_entropy: float = 0.0,
    batch: int = -1,
    update_grid: bool = False,
    singularity_avoiding: bool = True,
    log: int = 10,
) -> FitReport:
    """``safe_fit`` 的结构化报告版本。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        opt: 优化器名称，如 ``Adam`` 或 ``LBFGS``。
        steps: 训练步数。
        lr: 学习率。
        lamb: 稀疏正则权重。
        lamb_l1: L1 正则系数。
        lamb_entropy: 熵正则系数。
        batch: 批大小；``-1`` 表示全量。
        update_grid: 是否更新 grid。
        singularity_avoiding: 是否启用奇异点规避。
        log: 日志间隔。

    Returns:
        FitReport: 结构化结果，便于区分成功/失败/降级。
    """
    kw = dict(
        dataset=dataset,
        opt=opt,
        steps=steps,
        lr=lr,
        lamb=lamb,
        lamb_l1=lamb_l1,
        lamb_entropy=lamb_entropy,
        batch=batch,
        update_grid=update_grid,
        singularity_avoiding=singularity_avoiding,
        log=log,
    )
    if batch == -1:
        kw.pop("batch")

    _ensure_model_history_path(model)

    try:
        result = model.fit(**kw)
        return FitReport(success=True, result=result)
    except Exception as e:
        if "history.txt" in str(e):
            try:
                _ensure_model_history_path(model)
                result = model.fit(**kw)
                return FitReport(success=True, result=result, fallback_used="history_path_retry")
            except Exception as e_retry:
                e = e_retry

        if update_grid:
            kw["update_grid"] = False
            try:
                result = model.fit(**kw)
                return FitReport(success=True, result=result, fallback_used="grid_update_disabled")
            except Exception as e2:
                return FitReport(
                    success=False,
                    error_type=type(e2).__name__,
                    error_message=str(e2),
                    fallback_used="grid_update_disabled",
                )

        return FitReport(
            success=False,
            error_type=type(e).__name__,
            error_message=str(e),
        )
