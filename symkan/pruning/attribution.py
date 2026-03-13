"""symkan 特征归因与容错封装。

该模块包装 pykan 的 attribute 流程，统一处理推理模式冲突和失败回退。
"""

import numpy as np
import torch


def safe_attribute(model, dataset, n_sample: int = 2048):
    """安全执行归因计算并返回特征分数。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        n_sample: 参与归因计算的训练样本上限。

    Returns:
        numpy.ndarray: 特征分数向量，形状为 ``[input_dim]``。
    """
    was_training = bool(getattr(model, "training", False))
    model.eval()
    x = dataset["train_input"][:n_sample]

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
            # 某些 pykan 路径会在 inference_mode 下缓存反向图需要的中间张量，
            # 此时退回 no_grad 以保留前向所需状态。
            if "Inference tensors cannot be saved for backward" not in str(e):
                raise
            with torch.no_grad():
                _ = model(x, singularity_avoiding=True)
            _run_attribute()
    finally:
        model.train(was_training)

    score = model.feature_score.detach().cpu().numpy() if hasattr(model, "feature_score") else None
    if score is None:
        score = np.ones(model.width_in[0])
    return score


def safe_attribute_report(model, dataset, n_sample: int = 2048):
    """返回 ``safe_attribute`` 的结构化报告版本。

    Args:
        model: KAN/symkan 模型对象。
        dataset: 由 ``build_dataset`` 构建的数据字典。
        n_sample: 参与归因计算的训练样本上限。

    Returns:
        AttributeReport: 结构化归因结果。
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
