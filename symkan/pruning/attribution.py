import numpy as np
import torch


def safe_attribute(model, dataset, n_sample: int = 2048):
    """@brief 安全执行归因计算并返回特征分数。

    流程包括：
    1) 前向刷新内部激活状态；
    2) 调用 `attribute()` 计算归因；
    3) 在推理模式冲突时自动降级回退。

    @param model KAN/symkan 模型对象。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param n_sample 参与归因计算的训练样本上限。
    @return numpy.ndarray 特征分数向量，形状为 `[input_dim]`。
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
    """@brief safe_attribute 的结构化报告版本。

    @param model KAN/symkan 模型对象。
    @param dataset 由 `build_dataset` 构建的数据字典。
    @param n_sample 参与归因计算的训练样本上限。
    @return AttributeReport 结构化归因结果。
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
