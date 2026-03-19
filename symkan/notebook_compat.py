from __future__ import annotations

from typing import Any

from symkan.config.notebook import build_stagewise_notebook_config, build_symbolize_notebook_config
from symkan.symbolic.pipeline import symbolize_pipeline as _symbolize_pipeline_impl
from symkan.tuning.stagewise import stagewise_train as _stagewise_train_impl


def stagewise_train_from_notebook(dataset: dict[str, Any], **kwargs: Any):
    """Run stagewise_train from flat notebook-style kwargs.

    Args:
        dataset: Dataset dictionary already prepared for training.
        **kwargs: Notebook-style flat kwargs. Canonical parameter names are
            preferred; legacy aliases are accepted as fallback by
            ``symkan.config.notebook``.

    Returns:
        tuple[Any, dict[str, Any]]: The same return contract as
        ``symkan.tuning.stagewise.stagewise_train``.
    """
    config = build_stagewise_notebook_config(**kwargs)
    return _stagewise_train_impl(dataset, config)


def symbolize_pipeline_from_notebook(model: Any, dataset: dict[str, Any], **kwargs: Any):
    """Run symbolize_pipeline from flat notebook-style kwargs.

    Args:
        model: The fitted model to be symbolized.
        dataset: Dataset dictionary used by the symbolic pipeline.
        **kwargs: Notebook-style flat kwargs. Canonical parameter names are
            preferred; legacy aliases are accepted as fallback by
            ``symkan.config.notebook``.

    Returns:
        dict[str, Any]: The same result payload as
        ``symkan.symbolic.pipeline.symbolize_pipeline``.
    """
    config = build_symbolize_notebook_config(**kwargs)
    return _symbolize_pipeline_impl(model, dataset, config)
