"""Fault-tolerant feature attribution wrappers for symkan.

This module wraps pykan's ``attribute`` flow to centralize inference mode
conflict handling and fallback logic.
"""

import numpy as np
import torch

from symkan.core.infer import _infer_model_device


def safe_attribute(model, dataset, n_sample: int = 2048):
    """Safely compute feature attributions and return feature scores.

    Args:
        model: KAN/symkan model instance.
        dataset: Dataset dictionary produced by ``build_dataset``.
        n_sample: Maximum training samples used for attribution.

    Returns:
        numpy.ndarray: Feature score vector of shape ``[input_dim]``.
    """
    was_training = bool(getattr(model, "training", False))
    model.eval()
    model_device = _infer_model_device(model)
    x = dataset["train_input"][:n_sample]
    if not torch.is_tensor(x):
        x = torch.as_tensor(x, dtype=torch.float32, device=model_device)
    else:
        x = x.to(model_device)

    def _run_attribute():
        try:
            model.attribute(plot=False)
        except Exception:
            model.attribute()

    try:
        try:
            with torch.inference_mode():
                _ = model(x, singularity_avoiding=True)
            _run_attribute()
        except RuntimeError as e:
            # Some pykan paths cache backward tensors while in inference_mode,
            # so we retry under no_grad when that happens to avoid missing state.
            if "Inference tensors cannot be saved for backward" not in str(e):
                raise
            with torch.no_grad():
                _ = model(x, singularity_avoiding=True)
            _run_attribute()
    finally:
        model.train(was_training)

    feature_score = getattr(model, "feature_score", None)
    score = feature_score.detach().cpu().numpy() if feature_score is not None else None
    if score is None:
        raise RuntimeError(
            "attribute() finished without populating feature_score; "
            "cannot continue with implicit uniform feature ranking"
        )
    return score


def safe_attribute_report(model, dataset, n_sample: int = 2048):
    """Return a structured report for ``safe_attribute``.

    Args:
        model: KAN/symkan model instance.
        dataset: Dataset dictionary produced by ``build_dataset``.
        n_sample: Maximum training samples used for attribution.

    Returns:
        AttributeReport: Structured attribution result.
    """
    from symkan.core.types import AttributeReport

    try:
        score = safe_attribute(model, dataset, n_sample=n_sample)
        return AttributeReport(success=True, score=score)
    except Exception as exc:
        return AttributeReport(
            success=False,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
