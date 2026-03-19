"""Structured common types for symkan internals.

These dataclasses capture the structured objects passed across modules, avoiding
bare dictionaries and magic-string keys.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

import torch

from symkan.config import StagewiseConfig, SymbolizeConfig, TrainConfig


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

@dataclass
class DatasetBundle:
    """Structured dataset container that mirrors the legacy dict contract.

    Attributes:
        train_input: Training feature tensor.
        train_label: Training label tensor.
        test_input: Test feature tensor.
        test_label: Test label tensor.
        val_input: Optional validation feature tensor.
        val_label: Optional validation label tensor.
    """

    train_input: torch.Tensor
    train_label: torch.Tensor
    test_input: torch.Tensor
    test_label: torch.Tensor
    val_input: Optional[torch.Tensor] = None
    val_label: Optional[torch.Tensor] = None

    # ---- Legacy dict compatibility helpers ----

    def __getitem__(self, key: str) -> torch.Tensor:
        _MAP = {
            "train_input": "train_input",
            "train_label": "train_label",
            "val_input": "val_input",
            "val_label": "val_label",
            "test_input": "test_input",
            "test_label": "test_label",
        }
        attr = _MAP.get(key)
        if attr is None:
            raise KeyError(key)
        return getattr(self, attr)

    def __contains__(self, key: str) -> bool:
        return key in ("train_input", "train_label", "val_input", "val_label", "test_input", "test_label")

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetBundle":
        """Build a ``DatasetBundle`` from a legacy dataset dictionary.

        Args:
            d: Legacy dataset dictionary.

        Returns:
            DatasetBundle: Structured dataset wrapper.
        """
        return cls(
            train_input=d["train_input"],
            train_label=d["train_label"],
            val_input=d.get("val_input"),
            val_label=d.get("val_label"),
            test_input=d["test_input"],
            test_label=d["test_label"],
        )

    def to_dict(self) -> dict:
        """Convert the bundle back to the legacy dataset dictionary shape.

        Returns:
            dict: Legacy-compatible dataset mapping.
        """
        return {
            "train_input": self.train_input,
            "train_label": self.train_label,
            "val_input": self.val_input,
            "val_label": self.val_label,
            "test_input": self.test_input,
            "test_label": self.test_label,
        }


# ---------------------------------------------------------------------------
# Config objects
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Report / Result objects
# ---------------------------------------------------------------------------

@dataclass
class FitReport:
    """Structured result returned by guarded fit helpers.

    Attributes:
        success: Whether fitting succeeded.
        result: Raw fit payload returned by the model.
        fallback_used: Name of the fallback path used, if any.
        error_type: Exception type name when fitting failed.
        error_message: Human-readable failure message.
    """

    success: bool
    result: dict = field(default_factory=dict)
    fallback_used: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class AttributeReport:
    """Structured result returned by guarded attribution helpers.

    Attributes:
        success: Whether attribution succeeded.
        score: Attribution score array or tensor.
        fallback_used: Name of the fallback path used, if any.
        error_type: Exception type name when attribution failed.
        error_message: Human-readable failure message.
    """

    success: bool
    score: Any = None  # numpy array
    fallback_used: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class StageSnapshot:
    """Snapshot metadata recorded for a stagewise checkpoint candidate.

    Attributes:
        stage: Stage identifier.
        acc: Accuracy measured for the snapshot.
        n_edges: Edge count measured for the snapshot.
        score: Symbolic-readiness score for ranking snapshots.
        model: Optional cloned model payload.
    """

    stage: Union[int, str]
    acc: float
    n_edges: Union[int, float]
    score: float
    model: Any = None


@dataclass
class StagewiseResult:
    """Structured result returned by ``stagewise_train_report``.

    Attributes:
        best_model: Selected best model after stagewise ranking.
        train_loss: Aggregated training loss history.
        test_loss: Aggregated test loss history.
        stage_logs: Per-stage log records.
        best_acc: Accuracy of the selected snapshot.
        selected_stage: Identifier of the selected stage.
        selected_edges: Edge count of the selected snapshot.
        selected_score: Readiness score of the selected snapshot.
        best_state_dict: CPU-cloned state dict for the selected model.
        stage_snapshots: Recorded stage snapshot metadata.
        topk_models: Optional retained top-k model clones.
        stage_guard_mode: Guard mode used for pruning recovery.
        stage_early_stopped: Whether stagewise early stopping triggered.
        stage_early_stop_reason: Human-readable early-stop reason.
        stage_timings: Per-stage timing records.
        stage_train_total_seconds: Total training time across stages.
        stage_prune_total_seconds: Total pruning time across stages.
        final_finetune_seconds: Final fine-tune wall time.
        final_fit_success: Whether final fine-tuning succeeded.
        final_fit_error: Failure message for final fine-tuning, if any.
        successful_fit_count: Number of successful guarded fit operations.
        stage_total_seconds: Total wall time for stagewise training.
    """

    best_model: Any
    train_loss: List[float] = field(default_factory=list)
    test_loss: List[float] = field(default_factory=list)
    stage_logs: List[dict] = field(default_factory=list)
    best_acc: float = 0.0
    selected_stage: Union[int, str] = 0
    selected_edges: Union[int, float] = 0
    selected_score: float = 0.0
    best_state_dict: Optional[dict] = None
    stage_snapshots: List[dict] = field(default_factory=list)
    topk_models: Optional[List[dict]] = None
    stage_guard_mode: str = "light"
    stage_early_stopped: bool = False
    stage_early_stop_reason: str = ""
    stage_timings: List[dict] = field(default_factory=list)
    stage_train_total_seconds: float = 0.0
    stage_prune_total_seconds: float = 0.0
    final_finetune_seconds: float = 0.0
    final_fit_success: bool = False
    final_fit_error: str = ""
    successful_fit_count: int = 0
    stage_total_seconds: float = 0.0

    def to_legacy_dict(self) -> dict:
        """Convert the dataclass into a legacy dict for backward compatibility."""
        d = {
            "train_loss": self.train_loss,
            "test_loss": self.test_loss,
            "stage_logs": self.stage_logs,
            "best_acc": self.best_acc,
            "selected_stage": self.selected_stage,
            "selected_edges": self.selected_edges,
            "selected_score": self.selected_score,
            "best_state_dict": self.best_state_dict,
            "stage_snapshots": self.stage_snapshots,
            "stage_guard_mode": self.stage_guard_mode,
            "stage_early_stopped": self.stage_early_stopped,
            "stage_early_stop_reason": self.stage_early_stop_reason,
            "stage_timings": self.stage_timings,
            "stage_train_total_seconds": self.stage_train_total_seconds,
            "stage_prune_total_seconds": self.stage_prune_total_seconds,
            "final_finetune_seconds": self.final_finetune_seconds,
            "final_fit_success": self.final_fit_success,
            "final_fit_error": self.final_fit_error,
            "successful_fit_count": self.successful_fit_count,
            "stage_total_seconds": self.stage_total_seconds,
        }
        if self.topk_models is not None:
            d["topk_models"] = self.topk_models
        return d


@dataclass
class SymbolizeResult:
    """Structured result returned by ``symbolize_pipeline_report``.

    Attributes:
        model: Final symbolized model.
        formulas: Raw symbolic formula payload.
        valid_expressions: Filtered valid expressions with metadata.
        trace: Pruning trace table.
        sym_stats: Symbolic search statistics.
        final_n_edge: Effective final edge count.
        final_n_edge_raw: Raw final edge count reported by the model.
        final_acc: Final model accuracy after symbolization.
        effective_target_edges: Effective target used by the pipeline.
        input_n_edge: Input edge count before symbolic processing.
        effective_input_indices: Active input indices after compaction.
        effective_input_dim: Active input dimensionality after compaction.
        timing: Timing and warning diagnostics.
    """

    model: Any = None
    formulas: Any = None
    valid_expressions: List[dict] = field(default_factory=list)
    trace: Any = None  # DataFrame
    sym_stats: Dict[str, Any] = field(default_factory=dict)
    final_n_edge: Union[int, float] = 0
    final_n_edge_raw: Union[int, float] = 0
    final_acc: float = 0.0
    effective_target_edges: int = 0
    input_n_edge: Union[int, float] = 0
    effective_input_indices: List[int] = field(default_factory=list)
    effective_input_dim: int = 0
    timing: Dict[str, Any] = field(default_factory=dict)

    def to_legacy_dict(self) -> dict:
        """Convert the dataclass into a legacy dict for backward compatibility."""
        return {
            "model": self.model,
            "formulas": self.formulas,
            "valid_expressions": self.valid_expressions,
            "trace": self.trace,
            "sym_stats": self.sym_stats,
            "final_n_edge": self.final_n_edge,
            "final_n_edge_raw": self.final_n_edge_raw,
            "final_acc": self.final_acc,
            "effective_target_edges": self.effective_target_edges,
            "input_n_edge": self.input_n_edge,
            "effective_input_indices": self.effective_input_indices,
            "effective_input_dim": self.effective_input_dim,
            "timing": self.timing,
        }
