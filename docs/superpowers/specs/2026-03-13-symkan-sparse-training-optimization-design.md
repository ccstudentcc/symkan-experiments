# Symkan Sparse Training Optimization Design

**Date**: 2026-03-13
**Author**: Claude Code
**Status**: Draft
**Version**: 1.0

## 1. Executive Summary

This document outlines the design for optimizing sparse training in symkan, focusing on **Adaptive Threshold Control with Validation Feedback**. The optimization addresses two key pain points: pruning instability (accuracy drops and threshold selection difficulties) and slow convergence (excessive stages and fine-tuning). The primary objective is to improve final symbolic accuracy while respecting training time constraints.

## 2. Problem Analysis

### 2.1 Current Limitations
1. **Pruning instability**: Fixed threshold increments (`prune_edge_threshold_step`) lead to either overly conservative pruning (slow convergence) or aggressive pruning (accuracy drops).
2. **Slow convergence**: Many stagewise iterations required due to inefficient pruning schedule and excessive fine-tuning steps.
3. **Suboptimal regularization**: Fixed `lamb_schedule` doesn't adapt to current sparsity progress.

### 2.2 Root Causes
- **Threshold selection heuristic**: No feedback from pruning outcomes to inform future thresholds.
- **Lack of validation**: Pruning decisions based solely on training data, leading to overfitting to prune timing.
- **One-size-fits-all scheduling**: Same fine-tuning steps regardless of current model sparsity.

## 3. Design Goals

### 3.1 Primary Objectives
1. **Improve final symbolic accuracy** by 5-15% through more stable pruning
2. **Reduce training stages** by 20-40% through adaptive scheduling
3. **Minimize accuracy drops** from pruning by 30-50%

### 3.2 Constraints
- **Training time limited**: Optimization must not significantly increase total training time
- **Backward compatibility**: Existing code must continue to work with default parameters
- **Minimal complexity**: Solution should be understandable and maintainable

## 4. Architecture Overview

### 4.1 Core Components

#### 4.1.1 Validation Split System
- Creates 10-15% validation set from training data
- Used exclusively for prune impact assessment
- Optional feature with sensible default (enabled by default)

#### 4.1.2 Adaptive Threshold Controller
- Stateful controller tracking pruning success/failure patterns
- Dynamic threshold adjustment based on recent outcomes
- Configurable bounds to prevent extreme values

#### 4.1.3 Early Exit Criteria
- Monitors marginal sparsity gain per pruning attempt
- Stops pruning when gains fall below configurable threshold
- Prevents wasted computation on ineffective pruning

#### 4.1.4 Regularization Annealing
- Adjusts `lamb` based on current sparsity progress
- Higher regularization early, lower near target sparsity
- Fine-tuning steps scaled with sparsity ratio

### 4.2 Integration Points

```python
# Main integration in stagewise_train function
def stagewise_train(dataset, width, ..., adaptive_threshold=True, ...):
    # 1. Create validation split if not provided
    if use_validation and "val_input" not in dataset:
        dataset = _create_validation_split(dataset, validation_ratio)

    # 2. Initialize adaptive controller
    controller = AdaptiveThresholdController(
        base_step=threshold_base_step,
        min_threshold=threshold_min,
        max_threshold=threshold_max
    )

    # 3. During pruning phase
    while should_continue_pruning(controller, min_gain_threshold):
        current_threshold = controller.get_threshold()
        prune_result = attempt_prune_with_validation(
            model, dataset, current_threshold, ...
        )

        # 4. Update controller based on outcome
        controller.update(prune_result.success, prune_result.edges_removed)

        # 5. Adjust regularization based on sparsity
        current_lamb = compute_adaptive_lamb(
            base_lamb, current_edges, initial_edges, target_edges
        )
```

## 5. Detailed Component Design

### 5.1 Validation Split Implementation

#### 5.1.1 Option A: Extended Dataset Builder (Recommended)

**Location**: `symkan/core/data.py`

```python
def build_dataset_with_validation(
    Xtr, Ytr, Xte, Yte,
    validation_ratio=0.15,
    device=None,
    seed=None,
    min_val_samples=10
):
    """
    Build dataset with train/validation/test splits.

    Args:
        validation_ratio: Fraction of training data for validation (0.0-0.3)
        seed: Random seed for reproducible splits
        min_val_samples: Minimum validation samples; ratio adjusted if needed
    """
    if seed is not None:
        np.random.seed(seed)

    n_total = len(Xtr)

    # Ensure minimum validation samples
    n_val = int(n_total * validation_ratio)
    if n_val < min_val_samples and validation_ratio > 0:
        # Adjust ratio to meet minimum, but cap at 30%
        adjusted_ratio = min(min_val_samples / n_total, 0.3)
        if adjusted_ratio > validation_ratio:
            import warnings
            warnings.warn(
                f"Validation ratio adjusted from {validation_ratio:.3f} to {adjusted_ratio:.3f} "
                f"to ensure at least {min_val_samples} validation samples."
            )
            validation_ratio = adjusted_ratio
            n_val = int(n_total * validation_ratio)

    # If still insufficient or ratio is 0, disable validation
    if n_val < min_val_samples:
        n_val = 0
        if validation_ratio > 0:
            import warnings
            warnings.warn(
                f"Dataset too small for validation (n_total={n_total}). "
                f"Validation disabled."
            )

    if n_val == 0:
        # No validation split
        dataset = {
            "train_input": Xtr,
            "train_label": Ytr,
            "val_input": None,
            "val_label": None,
            "test_input": Xte,
            "test_label": Yte,
        }
    else:
        # Random permutation for split
        indices = np.random.permutation(n_total)
        val_idx, train_idx = indices[:n_val], indices[n_val:]

        dataset = {
            "train_input": Xtr[train_idx],
            "train_label": Ytr[train_idx],
            "val_input": Xtr[val_idx],
            "val_label": Ytr[val_idx],
            "test_input": Xte,
            "test_label": Yte,
        }

    # Move to device if specified
    if device is not None:
        dataset = _move_to_device(dataset, device)

    return dataset
```

#### 5.1.2 Option B: In-Place Split (Fallback)

If validation data not provided and `use_validation=True`, create split within `stagewise_train`:

```python
def _create_validation_split(dataset, ratio=0.15, min_val_samples=10):
    """Create validation split with edge case handling."""
    Xtr = dataset["train_input"]
    Ytr = dataset["train_label"]

    n_total = len(Xtr)
    n_val = int(n_total * ratio)

    # Ensure minimum validation samples
    if n_val < min_val_samples and ratio > 0:
        # Adjust ratio to meet minimum, but cap at 30%
        adjusted_ratio = min(min_val_samples / n_total, 0.3)
        if adjusted_ratio > ratio:
            import warnings
            warnings.warn(
                f"Validation ratio adjusted from {ratio:.3f} to {adjusted_ratio:.3f} "
                f"to ensure at least {min_val_samples} validation samples."
            )
            ratio = adjusted_ratio
            n_val = int(n_total * ratio)

    # If still insufficient or ratio is 0, disable validation
    if n_val < min_val_samples:
        n_val = 0
        if ratio > 0:
            import warnings
            warnings.warn(
                f"Dataset too small for validation (n_total={n_total}). "
                f"Validation disabled."
            )

    if n_val == 0:
        # No validation split, return original dataset structure
        return {
            "train_input": Xtr,
            "train_label": Ytr,
            "val_input": None,
            "val_label": None,
            "test_input": dataset["test_input"],
            "test_label": dataset["test_label"],
        }

    indices = torch.randperm(n_total)
    val_idx, train_idx = indices[:n_val], indices[n_val:]

    return {
        "train_input": Xtr[train_idx],
        "train_label": Ytr[train_idx],
        "val_input": Xtr[val_idx],
        "val_label": Ytr[val_idx],
        "test_input": dataset["test_input"],
        "test_label": dataset["test_label"],
    }
```

**Error Handling and Fallbacks**:
- If validation split fails (e.g., dataset too small), disable validation and continue with original logic
- If `safe_attribute` fails, fall back to default feature scores (all ones)
- If controller produces extreme threshold values, clamp to configured bounds
- If validation accuracy cannot be computed (no validation data), fall back to training accuracy for prune decisions
- All exceptions during adaptive pruning should be caught and logged, with fallback to original pruning logic

### 5.1.3 Extending Existing Functions

The optimization requires extending two existing functions to support validation data:

#### `model_acc_ds` Extension
The current `model_acc_ds` function in `symkan/core/infer.py` needs to support "val" split:

```python
def model_acc_ds(model, dataset, split: str = "test", device: Optional[str] = None):
    """Compute model accuracy for train/test/val splits."""
    try:
        return model_acc_ds_fast(model, dataset, split=split, device=device)
    except (KeyError, ValueError) as e:
        # Handle missing validation split by raising clear exception
        if split == "val":
            raise ValueError(f"Validation split ('val_input', 'val_label') not found in dataset. "
                           f"Ensure validation_ratio > 0 in build_dataset or disable validation.") from e
        raise

def model_acc_ds_fast(model, dataset, split: str = "test", device: Optional[str] = None):
    """Fast version with split validation."""
    if split not in dataset or dataset[split] is None:
        raise ValueError(f"Split '{split}' not available in dataset")

    # Existing implementation logic...
    # Use dataset[f"{split}_input"] and dataset[f"{split}_label"]
```

#### `build_dataset` Extension
The existing `build_dataset` function can be extended with optional validation split:

```python
def build_dataset(Xtr, Ytr, Xte, Yte, device=None, validation_ratio=0.0, seed=None):
    """Build dataset with optional validation split (backward compatible)."""
    # Existing logic for train/test split...

    # Add validation split if requested
    if validation_ratio > 0:
        # Use the logic from build_dataset_with_validation
        dataset["val_input"] = ...
        dataset["val_label"] = ...
    else:
        dataset["val_input"] = None
        dataset["val_label"] = None

    return dataset
```

**Backward Compatibility**: The extended functions maintain compatibility:
- `model_acc_ds(model, dataset)` defaults to "test" split
- `build_dataset(Xtr, Ytr, Xte, Yte)` defaults to `validation_ratio=0.0` (no validation)

#### Implementation Dependencies

The following existing functions and imports are required:

1. **Function Availability**:
   - `clone_model`: Import from `symkan.io.clone_model` (already used in `stagewise_train`)
   - `get_n_edge`: Import from `symkan.core.infer.get_n_edge`
   - `safe_fit`: Import from `symkan.core.train.safe_fit`
   - `safe_attribute`: Import from `symkan.pruning.attribution.safe_attribute`

2. **Parameter Verification**:
   - `safe_fit` must support `update_grid=False` parameter (verified in current implementation)
   - `model_acc_ds` must support `split` parameter (to be extended as described)
   - `build_dataset` must support `validation_ratio` parameter (to be extended as described)

3. **Error Handling**:
   - All new functions should catch and log exceptions appropriately
   - Fallback to original logic when validation data is unavailable
   - Warn users when validation is disabled due to insufficient data

4. **Testing Requirements**:
   - Verify extended functions maintain backward compatibility
   - Test validation split with various dataset sizes
   - Ensure `model_acc_ds` with "val" split doesn't break existing code

### 5.2 Adaptive Threshold Controller

#### 5.2.1 Controller State

```python
@dataclass
class AdaptiveThresholdController:
    """Stateful controller for adaptive threshold adjustment."""

    # Configuration
    base_step: float = 0.005
    min_threshold: float = 0.001
    max_threshold: float = 0.1
    success_boost: float = 0.5      # Multiplier per consecutive success
    failure_penalty: float = 0.3    # Multiplier per consecutive failure
    max_history: int = 10           # History length for trend analysis

    # State
    current_threshold: float = 0.005
    success_count: int = 0
    failure_count: int = 0
    history: List[Dict] = field(default_factory=list)
    total_prunes: int = 0
    total_successes: int = 0
```

#### 5.2.2 Adjustment Algorithm

```python
def adjust_threshold(self, success: bool, edges_removed: int) -> float:
    """Adjust threshold based on pruning outcome.

    Args:
        success: Whether the prune was accepted (validation drop within tolerance)
        edges_removed: Number of edges actually removed (0 if prune had no effect)

    Note:
        - If edges_removed == 0, treat as a failure for threshold adjustment
          (threshold too high or no edges below threshold)
        - The success flag still recorded for historical tracking
    """

    self.total_prunes += 1
    self.history.append({
        "threshold": self.current_threshold,
        "success": success,
        "edges_removed": edges_removed,
        "stage": self.total_prunes
    })

    # Keep history bounded
    if len(self.history) > self.max_history:
        self.history.pop(0)

    # Determine adjustment outcome
    # If no edges were removed, treat as failure (threshold too high)
    effective_success = success and (edges_removed > 0)

    # Update success/failure counters
    if effective_success:
        self.success_count += 1
        self.failure_count = 0
        self.total_successes += 1

        # More aggressive after consecutive successes
        boost = 1.0 + min(3.0, self.success_count * self.success_boost)
        increment = self.base_step * boost
        new_threshold = self.current_threshold + increment
    else:
        self.failure_count += 1
        self.success_count = 0

        # More conservative after failures
        penalty = 0.3 * (1.0 + min(2.0, self.failure_count * self.failure_penalty))
        decrement = self.base_step * penalty
        new_threshold = max(self.min_threshold, self.current_threshold - decrement)

    # Apply bounds
    new_threshold = np.clip(new_threshold, self.min_threshold, self.max_threshold)
    self.current_threshold = new_threshold

    return new_threshold
```

#### 5.2.3 Convergence Detection

```python
def should_continue(self, min_gain_threshold: int = 3) -> bool:
    """Determine if pruning should continue based on recent gains."""

    if len(self.history) < 3:
        return True

    # Calculate average edges removed in recent attempts
    recent = self.history[-3:]
    avg_gain = sum(h["edges_removed"] for h in recent) / len(recent)

    # Stop if gains are minimal
    if avg_gain < min_gain_threshold:
        return False

    # Stop if threshold is near maximum (diminishing returns)
    if self.current_threshold > self.max_threshold * 0.8:
        return False

    return True
```

### 5.3 Validation-Guided Pruning

#### 5.3.1 Prune Decision with Validation

```python
def attempt_prune_with_validation(
    model,
    dataset,
    threshold: float,
    current_lr: float,
    current_lamb: float,
    prune_acc_drop_tol: float = 0.03,
    post_prune_ft_steps: int = 40
) -> Dict:
    """Attempt pruning with validation-based acceptance check.

    Note: Validation data is used only for accuracy assessment, not for
    attribution or training. The safe_attribute function should continue
    to use only training data.
    """

    # Helper function to get validation accuracy with fallback and warning
    def _get_val_acc(split: str = "val"):
        """Get validation accuracy, fallback to training accuracy if validation not available."""
        try:
            return model_acc_ds(model, dataset, split=split)
        except (KeyError, ValueError) as e:
            # Validation split not available, fallback to training accuracy
            # This allows backward compatibility when validation is disabled
            import warnings
            warnings.warn(
                f"Validation split '{split}' not available in dataset. "
                f"Falling back to training accuracy for prune decisions. "
                f"Original error: {e}",
                category=UserWarning,
                stacklevel=2
            )
            return model_acc_ds(model, dataset, split="train")

    # 1. Save snapshot for rollback
    snapshot = clone_model(model)
    snapshot_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    acc_before_train = model_acc_ds(model, dataset, split="train")
    acc_before_val = _get_val_acc("val")

    # 2. Perform attribution and pruning (using only training data)
    # Note: safe_attribute internally uses dataset["train_input"]
    safe_attribute(model, dataset)
    edges_before = get_n_edge(model)
    model.prune_edge(threshold=threshold)
    edges_after = get_n_edge(model)
    edges_removed = edges_before - edges_after

    # 3. Short validation fine-tuning (if any edges were removed)
    if edges_removed > 0:
        # Use min(20, post_prune_ft_steps) for quick validation
        validation_ft_steps = min(20, post_prune_ft_steps) if post_prune_ft_steps >= 20 else post_prune_ft_steps
        safe_fit(
            model, dataset,
            steps=validation_ft_steps,
            lr=current_lr * 0.5,
            lamb=current_lamb * 0.1,
            update_grid=False
        )

    # 4. Check validation accuracy (with fallback)
    acc_after_val = _get_val_acc("val")
    val_drop = acc_before_val - acc_after_val

    # 5. Decision logic
    success = False
    if val_drop <= prune_acc_drop_tol:
        # Prune accepted - do full fine-tuning
        safe_fit(
            model, dataset,
            steps=post_prune_ft_steps,
            lr=current_lr * 0.5,
            lamb=current_lamb * 0.1,
            update_grid=False
        )
        success = True
    else:
        # Prune rejected - rollback to snapshot state
        model.load_state_dict(snapshot_state)
        edges_removed = 0

    return {
        "success": success,
        "edges_removed": edges_removed,
        "val_drop": val_drop,
        "threshold": threshold
    }
```

### 5.4 Regularization and Fine-Tuning Optimization

#### 5.4.1 Adaptive Regularization

```python
def compute_adaptive_lamb(
    base_lamb: float,
    current_edges: int,
    initial_edges: int,
    target_edges: int,
    min_lamb_ratio: float = 0.3,
    max_lamb_ratio: float = 1.5
) -> float:
    """Compute regularization strength based on sparsity progress."""

    if current_edges <= target_edges:
        return base_lamb * 0.2  # Very low when target reached

    sparsity_ratio = (initial_edges - current_edges) / (initial_edges - target_edges)
    sparsity_ratio = np.clip(sparsity_ratio, 0.0, 1.0)

    # Phase-based adjustment
    if sparsity_ratio < 0.3:
        # Early phase: encourage sparsity
        return base_lamb * max_lamb_ratio
    elif sparsity_ratio < 0.7:
        # Middle phase: neutral
        return base_lamb
    else:
        # Late phase: conserve accuracy
        return base_lamb * min_lamb_ratio
```

#### 5.4.2 Adaptive Fine-Tuning

```python
def compute_adaptive_ft_steps(
    base_steps: int,
    current_edges: int,
    initial_edges: int,
    target_edges: int,
    min_ratio: float = 0.3
) -> int:
    """Reduce fine-tuning steps as model becomes sparser."""

    if current_edges <= target_edges:
        return base_steps // 2

    sparsity_ratio = (initial_edges - current_edges) / (initial_edges - target_edges)
    sparsity_ratio = np.clip(sparsity_ratio, 0.0, 1.0)

    # Less recovery needed for sparser models
    steps_ratio = 1.0 - 0.7 * sparsity_ratio
    steps_ratio = max(min_ratio, steps_ratio)

    return int(base_steps * steps_ratio)
```

## 6. Configuration Interface

### 6.1 New Parameters for `stagewise_train`

```python
# Validation configuration
validation_ratio: float = 0.15           # Fraction for validation (0.0 to disable)
use_validation: bool = True              # Enable validation feedback
validation_seed: Optional[int] = None    # Seed for reproducible splits

# Adaptive threshold control
adaptive_threshold: bool = True          # Enable adaptive mode
threshold_base_step: float = 0.005       # Base increment step
threshold_min: float = 0.001             # Minimum threshold
threshold_max: float = 0.1               # Maximum threshold
success_boost: float = 0.5               # Multiplier per consecutive success
failure_penalty: float = 0.3             # Multiplier per consecutive failure

# Early exit criteria
min_gain_threshold: int = 3              # Stop if edges removed < this
max_prune_attempts: int = 20             # Maximum attempts per stage

# Regularization annealing
adaptive_lamb: bool = True               # Enable sparsity-aware regularization
min_lamb_ratio: float = 0.3              # Minimum lamb multiplier
max_lamb_ratio: float = 1.5              # Maximum lamb multiplier

# Fine-tuning optimization
adaptive_ft: bool = True                 # Adaptive fine-tuning steps
min_ft_ratio: float = 0.3                # Minimum fine-tuning steps ratio
```

### 6.2 Backward Compatibility

- **Default behavior**: All new parameters default to values that maintain backward compatibility
- **Migration path**:
  - Existing code: `stagewise_train(...)` works unchanged
  - Optimized code: `stagewise_train(..., adaptive_threshold=True, ...)`
- **Deprecation**: None - additive changes only

### 6.3 Parameter Grouping (Optional Enhancement)

For cleaner API and better organization, consider grouping related parameters into configuration objects. This is optional but recommended for long-term maintainability:

```python
@dataclass
class AdaptivePruningConfig:
    """Configuration for adaptive pruning features."""
    validation_ratio: float = 0.15
    use_validation: bool = True
    validation_seed: Optional[int] = None

    adaptive_threshold: bool = True
    threshold_base_step: float = 0.005
    threshold_min: float = 0.001
    threshold_max: float = 0.1
    success_boost: float = 0.5
    failure_penalty: float = 0.3

    min_gain_threshold: int = 3
    max_prune_attempts: int = 20

    adaptive_lamb: bool = True
    min_lamb_ratio: float = 0.3
    max_lamb_ratio: float = 1.5

    adaptive_ft: bool = True
    min_ft_ratio: float = 0.3

# Usage in stagewise_train
def stagewise_train(
    dataset,
    width,
    ...,
    adaptive_config: Optional[AdaptivePruningConfig] = None,
    **kwargs
):
    if adaptive_config is None:
        adaptive_config = AdaptivePruningConfig()
    # Use adaptive_config.validation_ratio, etc.
```

**Benefits**:
- Reduces function signature complexity
- Groups logically related parameters
- Enables easy configuration reuse across experiments
- Simplifies parameter validation and documentation

## 7. Expected Outcomes

### 7.1 Quantitative Targets

| Metric | Baseline | Target Improvement | Measurement Method |
|--------|----------|-------------------|-------------------|
| Pruning accuracy drops | 0.03-0.05 | 30-50% reduction | Compare `val_drop` distributions |
| Training stages to target | 8-12 stages | 20-40% reduction | Count stages to reach `target_edges` |
| Final symbolic accuracy | Variable | 5-15% improvement | Compare `final_acc` after symbolize_pipeline |
| Total training time | Baseline | 10-25% reduction | Wall-clock time measurement |
| Validation overhead | N/A | < 5% increase | Measure extra time for validation split & accuracy computation |

### 7.2 Qualitative Improvements

1. **More stable training**: Fewer catastrophic pruning events
2. **Better reproducibility**: Validation-guided decisions reduce randomness
3. **Easier tuning**: Fewer hyperparameters to manually adjust
4. **Improved user experience**: More predictable convergence behavior

## 8. Implementation Plan

### 8.1 Phase 1: Core Components (Week 1)
1. Implement `AdaptiveThresholdController` class
2. Add validation split to `build_dataset`
3. Create `attempt_prune_with_validation` function

### 8.2 Phase 2: Integration (Week 1)
1. Modify `stagewise_train` to use adaptive controller
2. Implement early exit logic
3. Add adaptive regularization and fine-tuning

### 8.3 Phase 3: Testing & Validation (Week 2)
1. Unit tests for controller logic
2. Integration tests with MNIST benchmark
3. Comparison against baseline across multiple seeds
4. Performance profiling

#### 8.3.1 Detailed Testing Strategy

**Unit Tests**:
- `AdaptiveThresholdController.adjust_threshold()`: Test with various success/failure patterns
- Edge cases: `edges_removed=0`, consecutive successes/failures, threshold bounds
- `should_continue()`: Test with different gain scenarios
- Validation split functions: Small datasets, edge ratios, seed reproducibility

**Integration Tests**:
- Compare adaptive vs fixed threshold on synthetic dataset
- Validate backward compatibility: ensure existing code works unchanged
- Test validation split integration with `safe_attribute` (ensure training data only)
- Measure accuracy drop reduction across multiple random seeds

**Edge Case Tests**:
- Very small datasets (< 100 samples) with validation split
- Already sparse models (edges near target)
- Extreme parameter values (very high/low thresholds)
- Disabled validation (`use_validation=False`)

**Performance Tests**:
- Wall-clock time comparison: adaptive vs baseline
- Memory usage with validation split and controller state
- Convergence speed: stages to reach target sparsity

**Regression Tests**:
- Ensure no degradation in final symbolic accuracy
- Verify symbolic pipeline still works with adapted models
- Test across different dataset sizes and complexities

### 8.4 Phase 4: Documentation & Examples (Week 2)
1. Update `symkan_usage.md` with new parameters
2. Create example notebook demonstrating benefits
3. Add configuration guidance for different use cases

## 9. Risk Assessment

### 9.1 Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Validation data reduces training performance | Low | Medium | Small ratio (10-15%), optional feature |
| Controller instability | Medium | Low | Conservative defaults, bounds checking |
| Increased code complexity | High | Low | Modular design, clear documentation |
| Performance overhead | Low | Low | Minimal validation computations |

### 9.2 Mitigation Strategies
1. **Feature flags**: All new features can be disabled
2. **Gradual rollout**: Test on subset of benchmarks first
3. **Fallback mechanisms**: Revert to original logic on error
4. **Comprehensive testing**: Validate across multiple datasets

## 10. Success Criteria

The optimization will be considered successful if:

1. **Primary**: Final symbolic accuracy improves by at least 5% on MNIST benchmark
2. **Secondary**: Training stages reduce by at least 20% to reach target sparsity
3. **Tertiary**: Pruning accuracy drops reduce by at least 30%
4. **Operational**: Backward compatibility maintained, no breaking changes

## 11. Appendices

### 11.1 References
- Current `stagewise_train` implementation: `symkan/tuning/stagewise.py`
- Original KAN pruning: `kan.MultKAN.prune_edge`
- Symkan documentation: `doc/symkan_usage.md`

### 11.2 Glossary
- **Sparsity ratio**: (initial_edges - current_edges) / (initial_edges - target_edges)
- **Validation drop**: Accuracy difference on validation set before/after prune
- **Marginal gain**: Average edges removed per recent pruning attempt
- **Adaptive threshold**: Dynamically adjusted pruning threshold based on outcomes