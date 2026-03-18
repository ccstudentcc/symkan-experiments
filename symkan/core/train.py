"""symkan 训练封装与容错原语。

从原 modeling.py 迁移。提供 safe_fit 及结构化训练报告。
"""

import os
from typing import Any

from .types import FitReport


class SafeFitError(RuntimeError):
    """Raised when a guarded fit operation fails in strict mode."""


def format_fit_failure(report: FitReport, context: str = "safe_fit") -> str:
    """Format a structured fit failure into a readable error message."""

    error_type = report.error_type or "FitError"
    error_message = report.error_message or "unknown fit failure"
    if report.fallback_used:
        return f"{context} failed after {report.fallback_used} ({error_type}: {error_message})"
    return f"{context} failed ({error_type}: {error_message})"


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


def _build_fit_kwargs(
    dataset,
    opt: str,
    steps: int,
    lr: float,
    lamb: float,
    lamb_l1: float,
    lamb_entropy: float,
    batch: int,
    update_grid: bool,
    singularity_avoiding: bool,
    log: int,
) -> dict[str, Any]:
    kw: dict[str, Any] = dict(
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
    return kw


def _run_fit(model, kw: dict[str, Any]) -> FitReport:
    try:
        result = model.fit(**kw)
        return FitReport(success=True, result=result)
    except Exception as exc:
        error = exc

    if "history.txt" in str(error):
        try:
            _ensure_model_history_path(model)
            result = model.fit(**kw)
            return FitReport(success=True, result=result, fallback_used="history_path_retry")
        except Exception as retry_exc:
            error = retry_exc

    if kw.get("update_grid", False):
        retry_kw = dict(kw)
        retry_kw["update_grid"] = False
        try:
            result = model.fit(**retry_kw)
            return FitReport(success=True, result=result, fallback_used="grid_update_disabled")
        except Exception as retry_exc:
            return FitReport(
                success=False,
                error_type=type(retry_exc).__name__,
                error_message=str(retry_exc),
                fallback_used="grid_update_disabled",
            )

    return FitReport(
        success=False,
        error_type=type(error).__name__,
        error_message=str(error),
    )


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
    raise_on_failure: bool = False,
    context: str = "safe_fit",
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
        raise_on_failure: 为 ``True`` 时，失败直接抛出 ``SafeFitError``。
        context: 失败消息中的上下文名称。

    Returns:
        dict: 训练过程结果字典（失败时返回空字典）。
    """
    _ensure_model_history_path(model)
    kw = _build_fit_kwargs(
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
    report = _run_fit(model, kw)
    if report.success:
        return report.result

    message = format_fit_failure(report, context=context)
    if raise_on_failure:
        raise SafeFitError(message)
    print(f"  [safe_fit] {message}，跳过")
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
    _ensure_model_history_path(model)
    kw = _build_fit_kwargs(
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
    return _run_fit(model, kw)
