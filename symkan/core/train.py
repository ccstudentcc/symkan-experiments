"""symkan training wrappers with resilience primitives.

Migrated from the original modeling.py; exposes ``safe_fit`` helpers
and structured training reports.
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
    """Ensure the pykan checkpoint history file exists before fitting.

    Args:
        model: Model-like object that may expose ``ckpt_path``.

    Returns:
        bool: ``True`` when a usable history path exists, otherwise ``False``.
    """
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
    """Build normalized keyword arguments for ``model.fit``.

    Args:
        dataset: Training dataset payload.
        opt: Optimizer name.
        steps: Number of fit steps.
        lr: Learning rate.
        lamb: Main sparsity regularization coefficient.
        lamb_l1: L1 regularization coefficient.
        lamb_entropy: Entropy regularization coefficient.
        batch: Batch size, where ``-1`` means full-batch.
        update_grid: Whether ``fit`` may update spline grids.
        singularity_avoiding: Whether singularity avoidance is enabled.
        log: Logging interval passed through to ``fit``.

    Returns:
        dict[str, Any]: Normalized kwargs ready for ``model.fit``.
    """
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
    """Run ``model.fit`` with built-in compatibility fallbacks.

    Args:
        model: Model-like object exposing ``fit``.
        kw: Normalized fit kwargs.

    Returns:
        FitReport: Structured result describing success, fallback usage, or
        failure details.
    """
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
    """Guarded training helper with automatic fallback logic.

    Args:
        model: KAN/symkan model object.
        dataset: Dataset dictionary from ``build_dataset``.
        opt: Optimizer name such as ``Adam`` or ``LBFGS``.
        steps: Number of training steps.
        lr: Learning rate.
        lamb: Sparsity regularization coefficient.
        lamb_l1: L1 regularization coefficient.
        lamb_entropy: Entropy regularization coefficient.
        batch: Batch size, where ``-1`` means full-batch.
        update_grid: Whether to allow ``fit`` to update spline grids.
        singularity_avoiding: Whether to enable singularity avoidance.
        log: Logging interval.
        raise_on_failure: When ``True``, raise ``SafeFitError`` on failure.
        context: Context label embedded in failure messages.

    Returns:
        dict: Training result payload (empty dict when failures are ignored).
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
    print(f"  [safe_fit] {message}, skipping")
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
    """Structured wrapper exposing ``safe_fit`` reports.

    Args:
        model: KAN/symkan model object.
        dataset: Dataset dictionary from ``build_dataset``.
        opt: Optimizer name such as ``Adam`` or ``LBFGS``.
        steps: Number of training steps.
        lr: Learning rate.
        lamb: Sparsity regularization coefficient.
        lamb_l1: L1 regularization coefficient.
        lamb_entropy: Entropy regularization coefficient.
        batch: Batch size, where ``-1`` means full-batch.
        update_grid: Whether to allow ``fit`` to update spline grids.
        singularity_avoiding: Whether to enable singularity avoidance.
        log: Logging interval.

    Returns:
        FitReport: Structured status describing success, failure, or fallbacks.
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
