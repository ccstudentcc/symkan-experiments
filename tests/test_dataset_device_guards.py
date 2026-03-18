from __future__ import annotations

import numpy as np
import pytest
import torch
from typing import Optional

from symkan.core.data import build_dataset
from symkan.core.infer import model_acc_ds, model_acc_ds_fast, model_logits, model_logits_ds
from symkan.pruning.attribution import safe_attribute


class FixedLogitModel(torch.nn.Module):
    def __init__(self, logits: torch.Tensor) -> None:
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(1))
        self._logits = logits

    def forward(self, x: torch.Tensor, singularity_avoiding: bool = True) -> torch.Tensor:
        rows = int(x.shape[0])
        return self._logits[:rows].to(x.device)


class MetaAttributeModel(torch.nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.empty(1, device="meta"))
        self.width_in = [input_dim]
        self.last_forward_device: Optional[torch.device] = None
        self.feature_score = None

    def forward(self, x: torch.Tensor, singularity_avoiding: bool = True) -> torch.Tensor:
        self.last_forward_device = x.device
        if x.device != self.anchor.device:
            raise RuntimeError(f"device mismatch: {x.device} vs {self.anchor.device}")
        return x

    def attribute(self, plot: bool = False) -> None:
        self.feature_score = torch.ones(self.width_in[0], dtype=torch.float32)


class TrainingStateTrackingModel(torch.nn.Module):
    def __init__(self, out_dim: int = 2) -> None:
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(1))
        self.out_dim = out_dim
        self.forward_training_flags: list[bool] = []

    def forward(self, x: torch.Tensor, singularity_avoiding: bool = True) -> torch.Tensor:
        self.forward_training_flags.append(bool(self.training))
        return torch.zeros((int(x.shape[0]), self.out_dim), dtype=torch.float32, device=x.device)


def test_build_dataset_accepts_1d_index_labels() -> None:
    dataset = build_dataset(
        np.array([[0.0], [1.0], [2.0]], dtype=np.float32),
        np.array([0, 1, 0], dtype=np.int64),
        np.array([[3.0], [4.0]], dtype=np.float32),
        np.array([1, 0], dtype=np.int64),
    )

    assert dataset["train_label"].shape == (3, 2)
    assert dataset["test_label"].shape == (2, 2)
    assert torch.equal(dataset["train_label"][1], torch.tensor([0.0, 1.0]))


def test_build_dataset_accepts_mixed_label_formats() -> None:
    dataset = build_dataset(
        np.array([[0.0], [1.0]], dtype=np.float32),
        np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32),
        np.array([[2.0], [3.0]], dtype=np.float32),
        np.array([1, 0], dtype=np.int64),
    )

    assert dataset["train_label"].shape == (2, 2)
    assert dataset["test_label"].shape == (2, 2)
    assert torch.equal(dataset["test_label"][0], torch.tensor([0.0, 1.0]))


def test_build_dataset_rejects_invalid_label_rank() -> None:
    with pytest.raises(ValueError, match="rank-1 class indices or rank-2"):
        build_dataset(
            np.array([[0.0], [1.0]], dtype=np.float32),
            np.zeros((2, 1, 1), dtype=np.float32),
            np.array([[2.0], [3.0]], dtype=np.float32),
            np.array([1, 0], dtype=np.int64),
        )


def test_build_dataset_rejects_invalid_validation_ratio() -> None:
    with pytest.raises(ValueError, match="validation_ratio must be in \\[0, 1\\)"):
        build_dataset(
            np.array([[0.0], [1.0]], dtype=np.float32),
            np.array([0, 1], dtype=np.int64),
            np.array([[2.0], [3.0]], dtype=np.float32),
            np.array([1, 0], dtype=np.int64),
            validation_ratio=1.0,
        )


def test_model_acc_ds_fast_accepts_1d_index_labels() -> None:
    dataset = {
        "test_input": torch.tensor([[0.0], [1.0], [2.0]], dtype=torch.float32),
        "test_label": torch.tensor([1, 0, 1], dtype=torch.int64),
    }
    model = FixedLogitModel(
        torch.tensor(
            [
                [0.1, 0.9],
                [0.8, 0.2],
                [0.3, 0.7],
            ],
            dtype=torch.float32,
        )
    )

    assert model_acc_ds_fast(model, dataset, split="test") == pytest.approx(1.0)


def test_model_acc_ds_fast_accepts_2d_one_hot_labels() -> None:
    dataset = {
        "test_input": torch.tensor([[0.0], [1.0]], dtype=torch.float32),
        "test_label": torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32),
    }
    model = FixedLogitModel(
        torch.tensor(
            [
                [0.8, 0.2],
                [0.1, 0.9],
            ],
            dtype=torch.float32,
        )
    )

    assert model_acc_ds_fast(model, dataset, split="test") == pytest.approx(1.0)


def test_model_acc_ds_rejects_invalid_label_rank() -> None:
    dataset = {
        "test_input": torch.tensor([[0.0], [1.0]], dtype=torch.float32),
        "test_label": torch.zeros((2, 1, 1), dtype=torch.float32),
    }
    model = FixedLogitModel(torch.tensor([[1.0], [1.0]], dtype=torch.float32))

    with pytest.raises(ValueError, match="rank-1 class indices or rank-2"):
        model_acc_ds(model, dataset, split="test")


def test_safe_attribute_moves_input_to_model_device() -> None:
    dataset = {
        "train_input": torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32),
        "train_label": torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32),
    }
    model = MetaAttributeModel(input_dim=2)

    score = safe_attribute(model, dataset, n_sample=1)

    assert model.last_forward_device == torch.device("meta")
    assert np.array_equal(score, np.ones(2, dtype=np.float32))


def test_model_logits_restores_training_mode_for_numpy_and_dataset_paths() -> None:
    model = TrainingStateTrackingModel(out_dim=2)
    model.train(True)

    logits_np = model_logits(model, np.array([[0.0], [1.0]], dtype=np.float32))

    assert model.training is True
    assert model.forward_training_flags == [False]
    assert logits_np.shape == (2, 2)

    model.forward_training_flags.clear()
    dataset = {
        "test_input": torch.tensor([[0.0], [1.0]], dtype=torch.float32),
        "test_label": torch.tensor([0, 1], dtype=torch.int64),
    }

    logits_ds = model_logits_ds(model, dataset, split="test")

    assert model.training is True
    assert model.forward_training_flags == [False]
    assert tuple(logits_ds.shape) == (2, 2)
