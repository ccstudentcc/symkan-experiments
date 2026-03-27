from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


_MNIST_FALLBACK_EXCEPTIONS = (ImportError, ModuleNotFoundError, OSError, RuntimeError, ValueError)

DEFAULT_SYMBOLNET_RUNS_DIR = "outputs/symbolnet_runs"
DEFAULT_SYMBOLNET_CONFIG_PATH = "configs/symbolnet/symbolnet.default.yaml"
CNN_BOOST_STABLE_LEARNING_RATE = 0.001
CNN_BOOST_STABLE_UNARY_OPS_CSV = "identity,square,cube,softsign"
CNN_BOOST_STABLE_ALPHA_SPARSITY_INPUT = 0.85
CNN_BOOST_STABLE_ALPHA_SPARSITY_MODEL = 0.95
CNN_BOOST_FORBIDDEN_UNARY_OPS = {"sin", "cos", "exp", "gauss", "sinh", "cosh", "tanh"}

np = None
fetch_openml = None
roc_auc_score = None
tf = None
keras = None
sympy_module = None


def _ensure_runtime_deps(require_tf: bool = False, require_openml: bool = False) -> None:
    global np, fetch_openml, roc_auc_score, tf, keras

    if np is None:
        import numpy as _np

        np = _np

    if require_openml and fetch_openml is None:
        from sklearn.datasets import fetch_openml as _fetch_openml

        fetch_openml = _fetch_openml

    if require_tf and tf is None:
        try:
            import tensorflow as _tf
            from tensorflow import keras as _keras
        except _MNIST_FALLBACK_EXCEPTIONS as exc:
            raise RuntimeError(
                "TensorFlow is required for SymbolNet training. "
                "Install dependencies from requirements.txt before running this command."
            ) from exc
        tf = _tf
        keras = _keras


def _parse_csv_ints(raw: str, arg_name: str) -> list[int]:
    values = [part.strip() for part in raw.split(",")]
    parsed: list[int] = []
    for part in values:
        if not part:
            continue
        try:
            parsed.append(int(part))
        except ValueError as exc:
            raise ValueError(f"invalid integer in {arg_name}: {part!r}") from exc
    if not parsed:
        raise ValueError(f"{arg_name} must contain at least one integer")
    return parsed


def _parse_csv_strs(raw: str) -> list[str]:
    values = [part.strip() for part in raw.split(",")]
    parsed = [part for part in values if part]
    if not parsed:
        raise ValueError("operator list must not be empty")
    return parsed


def _resolve_output_dir(raw: str, repo_root: Path) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root / candidate).resolve()


def _select_classes(x: Any, y: Any, classes: list[int]) -> tuple[Any, Any]:
    _ensure_runtime_deps()
    mask = np.zeros_like(y, dtype=bool)
    for cls in classes:
        mask |= y == int(cls)
    return x[mask], y[mask]


def _onehot_from_labels(y: Any, classes: list[int]) -> Any:
    _ensure_runtime_deps()
    class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
    mapped = np.array([class_to_idx[int(v)] for v in y], dtype=np.int64)
    return np.eye(len(classes), dtype=np.float32)[mapped]


def _fetch_mnist_via_keras(classes: list[int]) -> tuple[Any, Any, Any, Any]:
    _ensure_runtime_deps(require_tf=True)

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.reshape(x_train.shape[0], -1).astype(np.float32) / 255.0
    x_test = x_test.reshape(x_test.shape[0], -1).astype(np.float32) / 255.0
    y_train = y_train.astype(np.int64)
    y_test = y_test.astype(np.int64)

    x_train, y_train = _select_classes(x_train, y_train, classes)
    x_test, y_test = _select_classes(x_test, y_test, classes)
    y_train_onehot = _onehot_from_labels(y_train, classes)
    y_test_onehot = _onehot_from_labels(y_test, classes)
    return x_train, x_test, y_train_onehot, y_test_onehot


def _fetch_mnist_via_openml(classes: list[int]) -> tuple[Any, Any, Any, Any]:
    _ensure_runtime_deps(require_openml=True)
    mnist = fetch_openml("mnist_784", version=1, as_frame=False)
    x = mnist.data.astype(np.float32) / 255.0
    y = mnist.target.astype(np.int64)
    x_train, x_test = x[:60000], x[60000:]
    y_train, y_test = y[:60000], y[60000:]

    x_train, y_train = _select_classes(x_train, y_train, classes)
    x_test, y_test = _select_classes(x_test, y_test, classes)
    y_train_onehot = _onehot_from_labels(y_train, classes)
    y_test_onehot = _onehot_from_labels(y_test, classes)
    return x_train, x_test, y_train_onehot, y_test_onehot


def _fetch_mnist_with_fallback(classes: list[int]) -> tuple[tuple[Any, Any, Any, Any], str]:
    keras_error_message = ""
    try:
        return _fetch_mnist_via_keras(classes), "tensorflow.keras.datasets.mnist"
    except _MNIST_FALLBACK_EXCEPTIONS as keras_exc:
        keras_error_message = str(keras_exc)
        warnings.warn(
            f"[symbolnet] keras MNIST fetch failed ({keras_exc}); falling back to OpenML.",
            category=UserWarning,
            stacklevel=2,
        )

    try:
        return _fetch_mnist_via_openml(classes), "sklearn.fetch_openml(mnist_784)"
    except _MNIST_FALLBACK_EXCEPTIONS as openml_exc:
        raise RuntimeError(
            "automatic MNIST fetch failed via tensorflow.keras.datasets.mnist "
            f"({keras_error_message}) and sklearn.fetch_openml(mnist_784) ({openml_exc})"
        ) from openml_exc


def load_mnist_data(classes: list[int], max_train_samples: Optional[int], max_test_samples: Optional[int]) -> dict[str, Any]:
    _ensure_runtime_deps()
    (x_train, x_test, y_train, y_test), source = _fetch_mnist_with_fallback(classes)

    if max_train_samples is not None:
        x_train = x_train[: max(0, int(max_train_samples))]
        y_train = y_train[: max(0, int(max_train_samples))]
    if max_test_samples is not None:
        x_test = x_test[: max(0, int(max_test_samples))]
        y_test = y_test[: max(0, int(max_test_samples))]

    if x_train.shape[0] == 0 or x_test.shape[0] == 0:
        raise ValueError("dataset is empty after applying max_train_samples/max_test_samples")

    return {
        "X_train": x_train.astype(np.float32),
        "X_test": x_test.astype(np.float32),
        "Y_train": y_train.astype(np.float32),
        "Y_test": y_test.astype(np.float32),
        "classes": classes,
        "source": source,
        "input_dim": int(x_train.shape[1]),
        "output_dim": int(y_train.shape[1]),
    }


def _apply_cnn_boost(
    dataset: dict[str, Any],
    *,
    feature_dim: int,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    seed: int,
    quiet: bool,
) -> dict[str, Any]:
    _ensure_runtime_deps(require_tf=True)

    input_dim = int(dataset["input_dim"])
    side = int(round(math.sqrt(float(input_dim))))
    if side * side != input_dim:
        raise ValueError(
            f"CNN boost requires square image inputs; got input_dim={input_dim} "
            "(expected perfect square like 784 for MNIST)."
        )

    x_train = np.asarray(dataset["X_train"], dtype=np.float32)
    x_test = np.asarray(dataset["X_test"], dtype=np.float32)
    y_train_onehot = np.asarray(dataset["Y_train"], dtype=np.float32)
    y_test_onehot = np.asarray(dataset["Y_test"], dtype=np.float32)
    y_train_cls = np.argmax(y_train_onehot, axis=1).astype(np.int64)
    y_test_cls = np.argmax(y_test_onehot, axis=1).astype(np.int64)

    x_train_img = x_train.reshape((-1, side, side, 1)).astype(np.float32)
    x_test_img = x_test.reshape((-1, side, side, 1)).astype(np.float32)

    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

    inputs = keras.Input(shape=(side, side, 1), name="symbolnet_cnn_input")
    x = keras.layers.Conv2D(16, kernel_size=3, padding="same", activation="relu")(inputs)
    x = keras.layers.MaxPool2D(pool_size=2)(x)
    x = keras.layers.Conv2D(32, kernel_size=3, padding="same", activation="relu")(x)
    x = keras.layers.MaxPool2D(pool_size=2)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(128, activation="relu")(x)
    feature = keras.layers.Dense(int(feature_dim), activation="relu", name="symbolnet_cnn_feature")(x)
    logits = keras.layers.Dense(int(dataset["output_dim"]), activation="softmax", name="symbolnet_cnn_head")(feature)

    cnn_model = keras.Model(inputs=inputs, outputs=logits, name="symbolnet_cnn_boost")
    cnn_model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=float(learning_rate)),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    cnn_model.fit(
        x_train_img,
        y_train_cls,
        validation_data=(x_test_img, y_test_cls),
        epochs=int(epochs),
        batch_size=int(batch_size),
        verbose=0 if quiet else 1,
    )

    feature_model = keras.Model(
        inputs=cnn_model.input,
        outputs=cnn_model.get_layer("symbolnet_cnn_feature").output,
        name="symbolnet_cnn_feature_extractor",
    )
    x_train_feature = feature_model.predict(x_train_img, batch_size=int(batch_size), verbose=0).astype(np.float32)
    x_test_feature = feature_model.predict(x_test_img, batch_size=int(batch_size), verbose=0).astype(np.float32)

    feat_mean = np.mean(x_train_feature, axis=0, keepdims=True).astype(np.float32)
    feat_std = np.std(x_train_feature, axis=0, keepdims=True).astype(np.float32) + np.float32(1e-6)
    x_train_feature = ((x_train_feature - feat_mean) / feat_std).astype(np.float32)
    x_test_feature = ((x_test_feature - feat_mean) / feat_std).astype(np.float32)

    boosted = dict(dataset)
    boosted["X_train"] = x_train_feature
    boosted["X_test"] = x_test_feature
    boosted["raw_input_dim"] = int(input_dim)
    boosted["input_dim"] = int(x_train_feature.shape[1])
    boosted["source"] = (
        f"{dataset.get('source', 'unknown')} + cnn_boost(dim={int(feature_dim)},epochs={int(epochs)})"
    )
    boosted["cnn_boost"] = {
        "enabled": True,
        "feature_dim": int(feature_dim),
        "epochs": int(epochs),
        "batch_size": int(batch_size),
        "learning_rate": float(learning_rate),
        "seed": int(seed),
    }
    return boosted


def _ensure_sympy_dep() -> Any:
    global sympy_module
    if sympy_module is None:
        import sympy as _sympy

        sympy_module = _sympy
    return sympy_module


def _compute_class_auc_ovr(y_true_onehot: Any, y_pred_prob: Any) -> tuple[dict[int, float], float]:
    _ensure_runtime_deps()
    global roc_auc_score
    if roc_auc_score is None:
        try:
            from sklearn.metrics import roc_auc_score as _roc_auc_score
        except Exception:
            _roc_auc_score = None
        roc_auc_score = _roc_auc_score

    n_classes = int(y_true_onehot.shape[1])
    class_auc: dict[int, float] = {}
    for class_idx in range(n_classes):
        if roc_auc_score is None:
            class_auc[class_idx] = float("nan")
            continue
        try:
            class_auc[class_idx] = float(roc_auc_score(y_true_onehot[:, class_idx], y_pred_prob[:, class_idx]))
        except Exception:
            class_auc[class_idx] = float("nan")

    finite_values = [value for value in class_auc.values() if math.isfinite(value)]
    macro_auc = float(np.mean(finite_values)) if finite_values else float("nan")
    return class_auc, macro_auc


def _math_operation_sympy(operator: str, x: Any, y: Any = None) -> Any:
    sympy = _ensure_sympy_dep()
    if operator == "identity":
        return x
    if operator == "sin":
        return sympy.sin(x)
    if operator == "cos":
        return sympy.cos(x)
    if operator == "exp":
        return sympy.exp(x)
    if operator == "gauss":
        return sympy.exp(-(x**2))
    if operator == "sinh":
        return sympy.sinh(x)
    if operator == "cosh":
        return sympy.cosh(x)
    if operator == "tanh":
        return sympy.tanh(x)
    if operator == "square":
        return x**2
    if operator == "cube":
        return x**3
    if operator == "softsign":
        return x / (1 + sympy.Abs(x))
    if operator == "log":
        return sympy.log(0.001 + sympy.Abs(x))
    if operator == "+":
        return x + y
    if operator == "*":
        return x * y
    if operator == "pow":
        return x**y
    if operator == "/":
        return x / (0.001 + sympy.Abs(y))
    raise ValueError(f"unsupported sympy operator: {operator}")


def math_operation(mode: str, operator: str, x: Any, y: Any = None) -> Any:
    if operator == "identity":
        return x
    if operator == "sin":
        return tf.sin(x) if mode == "tf" else np.sin(x)
    if operator == "cos":
        return tf.cos(x) if mode == "tf" else np.cos(x)
    if operator == "exp":
        return tf.exp(x) if mode == "tf" else np.exp(x)
    if operator == "gauss":
        return tf.exp(-(x**2)) if mode == "tf" else np.exp(-(x**2))
    if operator == "sinh":
        return tf.sinh(x) if mode == "tf" else np.sinh(x)
    if operator == "cosh":
        return tf.cosh(x) if mode == "tf" else np.cosh(x)
    if operator == "tanh":
        return tf.tanh(x) if mode == "tf" else np.tanh(x)
    if operator == "square":
        return x**2
    if operator == "cube":
        return x**3
    if operator == "softsign":
        return x / (1.0 + tf.abs(x)) if mode == "tf" else x / (1.0 + np.abs(x))
    if operator == "log":
        return tf.math.log(0.001 + tf.abs(x)) if mode == "tf" else np.log(0.001 + np.abs(x))
    if operator == "+":
        return x + y
    if operator == "*":
        return x * y
    if operator == "pow":
        return x**y
    if operator == "/":
        return x / (0.001 + tf.abs(y)) if mode == "tf" else x / (0.001 + np.abs(y))
    raise ValueError(f"unsupported operator: {operator}")


def _build_step_func() -> Any:
    @tf.custom_gradient
    def _step_func(x: Any) -> Any:
        func = tf.where(x > 0.0, 1.0, 0.0)

        def grad(upstream: Any) -> Any:
            a = tf.cast(5.0, dtype=x.dtype)
            return upstream * a * tf.exp(-a * x) / (1.0 + tf.exp(-a * x)) ** 2

        return func, grad

    return _step_func


def _build_symbolnet_model(
    input_dim: int,
    output_dim: int,
    num_hidden_layers: int,
    unary_ops: list[str],
    binary_ops: list[str],
    num_unary: int,
    num_binary: int,
) -> tuple[Any, list[int], list[list[list[str]]], list[list[int]]]:
    step_func = _build_step_func()

    class InputSparsity(keras.layers.Layer):
        def build(self, input_shape: Any) -> None:
            self.aux_w = self.add_weight(
                name="weight",
                shape=(int(input_shape[-1]),),
                initializer="ones",
                trainable=False,
            )
            self.aux_w_t = self.add_weight(
                name="threshold",
                shape=(int(input_shape[-1]),),
                initializer="zeros",
                constraint=lambda x: tf.clip_by_value(x, 0.0, 1.0),
                trainable=True,
            )

        def call(self, inputs: Any) -> Any:
            input_masks = step_func(self.aux_w - self.aux_w_t)
            return tf.multiply(inputs, input_masks)

    class SymbolicLayer(keras.layers.Layer):
        def __init__(self, operators: list[list[str]], num_operators: list[int], **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.operators = operators
            self.num_operators = num_operators
            self.num_unary = int(num_operators[0])
            self.num_binary = int(num_operators[1])
            self.units = self.num_unary + 2 * self.num_binary

        def build(self, input_shape: Any) -> None:
            width = int(input_shape[-1])
            self.w = self.add_weight(
                name="weight",
                shape=(width, self.units),
                initializer="random_normal",
                trainable=True,
            )
            self.b = self.add_weight(
                name="bias",
                shape=(self.units,),
                initializer="random_normal",
                trainable=True,
            )
            self.aux_unary = self.add_weight(
                name="unary",
                shape=(self.num_unary,),
                initializer="ones",
                trainable=False,
            )
            self.aux_w_t = self.add_weight(
                name="weight_threshold",
                shape=(width, self.units),
                initializer="zeros",
                constraint=lambda x: tf.abs(x),
                trainable=True,
            )
            self.aux_b_t = self.add_weight(
                name="bias_threshold",
                shape=(self.units,),
                initializer="zeros",
                constraint=lambda x: tf.abs(x),
                trainable=True,
            )
            self.aux_unary_t = self.add_weight(
                name="unary_threshold",
                shape=(self.num_unary,),
                initializer="zeros",
                constraint=lambda x: tf.clip_by_value(x, 0.0, 1.0),
                trainable=True,
            )
            if self.num_binary > 0:
                self.aux_binary = self.add_weight(
                    name="binary",
                    shape=(self.num_binary,),
                    initializer="ones",
                    trainable=False,
                )
                self.aux_binary_t = self.add_weight(
                    name="binary_threshold",
                    shape=(self.num_binary,),
                    initializer="zeros",
                    constraint=lambda x: tf.clip_by_value(x, 0.0, 1.0),
                    trainable=True,
                )

        def call(self, inputs: Any) -> Any:
            w_masks = step_func(tf.abs(self.w) - self.aux_w_t)
            b_masks = step_func(tf.abs(self.b) - self.aux_b_t)
            linear_output = tf.matmul(inputs, tf.multiply(self.w, w_masks)) + tf.multiply(self.b, b_masks)

            symbolic_output = []
            unary_ops_local = self.operators[0]
            for i in range(self.num_unary):
                unary_mask = step_func(self.aux_unary - self.aux_unary_t)[i]
                op = unary_ops_local[i % len(unary_ops_local)]
                unary_operation = (
                    unary_mask * math_operation("tf", op, linear_output[:, i : i + 1])
                    + (1.0 - unary_mask) * math_operation("tf", "identity", linear_output[:, i : i + 1])
                )
                symbolic_output.append(unary_operation)

            if self.num_binary > 0:
                binary_ops_local = self.operators[1]
                for j in range(self.num_binary):
                    col = self.num_unary + 2 * j
                    left = linear_output[:, col : col + 1]
                    right = linear_output[:, col + 1 : col + 2]
                    binary_mask = step_func(self.aux_binary - self.aux_binary_t)[j]
                    op = binary_ops_local[j % len(binary_ops_local)]
                    binary_operation = (
                        binary_mask * math_operation("tf", op, left, right)
                        + (1.0 - binary_mask) * math_operation("tf", "+", left, right)
                    )
                    symbolic_output.append(binary_operation)

            return tf.concat(symbolic_output, axis=1)

    model_dim = [int(input_dim), int(num_hidden_layers), int(output_dim)]
    operators = [[list(unary_ops), list(binary_ops)] for _ in range(num_hidden_layers)]
    num_operators = [[int(num_unary), int(num_binary)] for _ in range(num_hidden_layers)]

    inputs = keras.Input(shape=(input_dim,))
    x = InputSparsity(name="input_sparsity")(inputs)
    for layer_idx in range(num_hidden_layers):
        x = SymbolicLayer(
            operators=operators[layer_idx],
            num_operators=num_operators[layer_idx],
            name=f"symbolic_layer_{layer_idx + 1}",
        )(x)
    x = SymbolicLayer(
        operators=[["identity"], []],
        num_operators=[output_dim, 0],
        name="symbolic_output_layer",
    )(x)
    model = keras.Model(inputs=inputs, outputs=x, name="symbolnet")
    return model, model_dim, operators, num_operators


def _build_neural_sr(
    model: Any,
    model_dim: list[int],
    operators: list[list[list[str]]],
    num_operators: list[list[int]],
    alpha_sparsity_input: float,
    alpha_sparsity_model: float,
    alpha_sparsity_unary: float,
    alpha_sparsity_binary: float,
) -> Any:
    class NeuralSR(keras.Model):
        def __init__(self) -> None:
            super().__init__()
            self.symbolic_model = model
            self.model_dim = model_dim
            self.operators = operators
            self.num_operators = num_operators
            self.alpha_sparsity_input = float(alpha_sparsity_input)
            self.alpha_sparsity_model = float(alpha_sparsity_model)
            self.alpha_sparsity_unary = float(alpha_sparsity_unary)
            self.alpha_sparsity_binary = float(alpha_sparsity_binary)

            self.total_loss_tracker = keras.metrics.Mean(name="loss")
            self.regression_loss_tracker = keras.metrics.Mean(name="regression_loss")
            self.sparsity_input_tracker = keras.metrics.Mean(name="sparsity_input")
            self.sparsity_model_tracker = keras.metrics.Mean(name="sparsity_model")
            self.sparsity_unary_tracker = keras.metrics.Mean(name="sparsity_unary")
            self.sparsity_binary_tracker = keras.metrics.Mean(name="sparsity_binary")
            self.accuracy_tracker = keras.metrics.CategoricalAccuracy(name="accuracy")

        @property
        def metrics(self) -> list[Any]:
            return [
                self.total_loss_tracker,
                self.regression_loss_tracker,
                self.sparsity_input_tracker,
                self.sparsity_model_tracker,
                self.sparsity_unary_tracker,
                self.sparsity_binary_tracker,
                self.accuracy_tracker,
            ]

        def call(self, inputs: Any, training: bool = False) -> Any:
            return self.symbolic_model(inputs, training=training)

        def train_step(self, data: tuple[Any, Any]) -> dict[str, Any]:
            x, y = data
            with tf.GradientTape() as tape:
                y_pred = self.symbolic_model(x, training=True)
                regression_loss = tf.reduce_mean(
                    tf.reduce_sum(tf.cast((y - y_pred) ** 2, dtype=tf.float64), axis=1)
                )

                input_layer = self.symbolic_model.get_layer("input_sparsity")
                w_input = input_layer.aux_w
                w_t_input = input_layer.aux_w_t
                num_input_masks = tf.reduce_sum(tf.cast(tf.where(w_input - w_t_input > 0.0, 0.0, 1.0), tf.float64))
                num_input_weights = tf.cast(tf.size(w_input), tf.float64)
                sparsity_input = tf.math.divide_no_nan(num_input_masks, num_input_weights)
                threshold_input_mean = tf.math.divide_no_nan(
                    tf.reduce_sum(tf.cast(w_t_input, tf.float64)),
                    num_input_weights,
                )

                symbolic_layers = [layer for layer in self.symbolic_model.layers if hasattr(layer, "num_unary")]

                num_model_masks = tf.cast(0.0, tf.float64)
                num_model_weights = tf.cast(0.0, tf.float64)
                sum_exp_t = tf.cast(0.0, tf.float64)
                num_unary_masks = tf.cast(0.0, tf.float64)
                num_unary_weights = tf.cast(0.0, tf.float64)
                num_binary_masks = tf.cast(0.0, tf.float64)
                num_binary_weights = tf.cast(0.0, tf.float64)

                for layer in symbolic_layers:
                    sum_exp_t += tf.reduce_sum(tf.exp(-tf.cast(layer.aux_w_t, tf.float64)))
                    sum_exp_t += tf.reduce_sum(tf.exp(-tf.cast(layer.aux_b_t, tf.float64)))

                    num_model_masks += tf.reduce_sum(
                        tf.cast(tf.where(tf.abs(layer.w) - layer.aux_w_t > 0.0, 0.0, 1.0), tf.float64)
                    )
                    num_model_masks += tf.reduce_sum(
                        tf.cast(tf.where(tf.abs(layer.b) - layer.aux_b_t > 0.0, 0.0, 1.0), tf.float64)
                    )
                    num_model_weights += tf.cast(tf.size(layer.w), tf.float64)
                    num_model_weights += tf.cast(tf.size(layer.b), tf.float64)

                hidden_layers = symbolic_layers[:-1]
                for layer in hidden_layers:
                    num_unary_masks += tf.reduce_sum(
                        tf.cast(tf.where(layer.aux_unary - layer.aux_unary_t > 0.0, 0.0, 1.0), tf.float64)
                    )
                    num_unary_weights += tf.cast(tf.size(layer.aux_unary), tf.float64)
                    if layer.num_binary > 0:
                        num_binary_masks += tf.reduce_sum(
                            tf.cast(tf.where(layer.aux_binary - layer.aux_binary_t > 0.0, 0.0, 1.0), tf.float64)
                        )
                        num_binary_weights += tf.cast(tf.size(layer.aux_binary), tf.float64)

                sparsity_model = tf.math.divide_no_nan(num_model_masks, num_model_weights)
                sparsity_unary = tf.math.divide_no_nan(num_unary_masks, num_unary_weights)
                sparsity_binary = tf.math.divide_no_nan(num_binary_masks, num_binary_weights)

                threshold_model_reg_loss = regression_loss * tf.math.divide_no_nan(sum_exp_t, num_model_weights)
                threshold_input_reg_loss = regression_loss * tf.exp(-threshold_input_mean)
                threshold_unary_reg_loss = regression_loss * tf.exp(-sparsity_unary)
                threshold_binary_reg_loss = regression_loss * tf.exp(-sparsity_binary)

                def _reg(s: Any, s_t: float, d: float) -> Any:
                    s_t_tf = tf.cast(s_t, dtype=tf.float64)
                    denominator = tf.maximum(s_t_tf - tf.minimum(s, s_t_tf), tf.cast(1e-6, tf.float64))
                    return tf.exp(-(s_t_tf / denominator) ** tf.cast(d, tf.float64) + tf.cast(1.0, tf.float64))

                threshold_input_reg_loss *= _reg(sparsity_input, self.alpha_sparsity_input, 0.01)
                threshold_model_reg_loss *= _reg(sparsity_model, self.alpha_sparsity_model, 0.01)
                threshold_unary_reg_loss *= _reg(sparsity_unary, self.alpha_sparsity_unary, 0.01)
                threshold_binary_reg_loss *= _reg(sparsity_binary, self.alpha_sparsity_binary, 0.01)

                total_loss = (
                    regression_loss
                    + threshold_input_reg_loss
                    + threshold_model_reg_loss
                    + threshold_unary_reg_loss
                    + threshold_binary_reg_loss
                )

            trainable_weights = self.symbolic_model.trainable_weights
            grads = tape.gradient(total_loss, trainable_weights)
            self.optimizer.apply_gradients(zip(grads, trainable_weights))

            self.total_loss_tracker.update_state(total_loss)
            self.regression_loss_tracker.update_state(regression_loss)
            self.sparsity_input_tracker.update_state(sparsity_input)
            self.sparsity_model_tracker.update_state(sparsity_model)
            self.sparsity_unary_tracker.update_state(sparsity_unary)
            self.sparsity_binary_tracker.update_state(sparsity_binary)
            self.accuracy_tracker.update_state(y, y_pred)

            return {metric.name: metric.result() for metric in self.metrics}

    return NeuralSR()


def train_symbolnet_once(runner: "SymbolNetRunnerConfig", dataset: dict[str, Any], seed: int) -> dict[str, Any]:
    _ensure_runtime_deps(require_tf=True)

    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

    model, model_dim, operators, num_operators = _build_symbolnet_model(
        input_dim=dataset["input_dim"],
        output_dim=dataset["output_dim"],
        num_hidden_layers=runner.num_hidden_layers,
        unary_ops=runner.unary_ops,
        binary_ops=runner.binary_ops,
        num_unary=runner.num_unary,
        num_binary=runner.num_binary,
    )
    nsr = _build_neural_sr(
        model=model,
        model_dim=model_dim,
        operators=operators,
        num_operators=num_operators,
        alpha_sparsity_input=runner.alpha_sparsity_input,
        alpha_sparsity_model=runner.alpha_sparsity_model,
        alpha_sparsity_unary=runner.alpha_sparsity_unary,
        alpha_sparsity_binary=runner.alpha_sparsity_binary,
    )
    nsr.compile(optimizer=keras.optimizers.Adam(learning_rate=runner.learning_rate))

    train_start = time.perf_counter()
    fit_result = nsr.fit(
        dataset["X_train"],
        dataset["Y_train"],
        epochs=runner.epochs,
        batch_size=runner.batch_size,
        verbose=0 if runner.quiet else 1,
    )
    train_seconds = float(time.perf_counter() - train_start)

    predict_start = time.perf_counter()
    y_pred = nsr.symbolic_model.predict(dataset["X_test"], batch_size=runner.batch_size, verbose=0)
    predict_seconds = float(time.perf_counter() - predict_start)

    y_true = np.argmax(dataset["Y_test"], axis=1)
    y_hat = np.argmax(y_pred, axis=1)
    acc = float(np.mean(y_true == y_hat))
    class_auc, auc_macro = _compute_class_auc_ovr(dataset["Y_test"], y_pred)

    history = {name: [float(v) for v in values] for name, values in fit_result.history.items()}
    return {
        "history": history,
        "accuracy": acc,
        "macro_auc_ovr": auc_macro,
        "class_auc": class_auc,
        "train_seconds": train_seconds,
        "predict_seconds": predict_seconds,
        "samples_train": int(dataset["X_train"].shape[0]),
        "samples_test": int(dataset["X_test"].shape[0]),
        "symbolic_model": nsr.symbolic_model,
        "model_dim": model_dim,
        "operators": operators,
        "num_operators": num_operators,
    }


def _write_history_csv(path: Path, history: dict[str, list[float]]) -> None:
    columns = list(history.keys())
    max_len = max((len(values) for values in history.values()), default=0)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epoch"] + columns)
        writer.writeheader()
        for idx in range(max_len):
            row: dict[str, Any] = {"epoch": idx + 1}
            for column in columns:
                values = history.get(column, [])
                row[column] = values[idx] if idx < len(values) else ""
            writer.writerow(row)


def _write_metrics_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def _build_symbolic_summary_rows(
    *,
    model: Any,
    model_dim: list[int],
    operators: list[list[list[str]]],
    num_operators: list[list[int]],
    class_auc: dict[int, float],
    significant_digits: int = 2,
) -> list[dict[str, Any]]:
    _ensure_runtime_deps()
    sympy = _ensure_sympy_dep()

    input_dim, num_hidden_layers, output_dim = model_dim
    x_symbols = [sympy.Symbol(f"x_{idx}") for idx in range(input_dim)]
    x_masked = sympy.Matrix([x_symbols])

    input_layer = model.get_layer("input_sparsity")
    input_weight = np.asarray(input_layer.aux_w.numpy(), dtype=np.float64)
    input_threshold = np.asarray(input_layer.aux_w_t.numpy(), dtype=np.float64)
    input_mask = np.where(input_weight - input_threshold > 0.0, 1.0, 0.0)
    x_masked = sympy.Matrix([[sympy.Float(float(input_mask[idx])) * x_symbols[idx] for idx in range(input_dim)]])

    hidden_layers = [model.get_layer(f"symbolic_layer_{idx + 1}") for idx in range(num_hidden_layers)]
    output_layer = model.get_layer("symbolic_output_layer")
    layers = hidden_layers + [output_layer]

    for layer_idx, layer in enumerate(layers):
        weight = np.asarray(layer.w.numpy(), dtype=np.float64)
        bias = np.asarray(layer.b.numpy(), dtype=np.float64)
        weight_threshold = np.asarray(layer.aux_w_t.numpy(), dtype=np.float64)
        bias_threshold = np.asarray(layer.aux_b_t.numpy(), dtype=np.float64)

        weight_masked = np.where(np.abs(weight) - weight_threshold > 0.0, weight, 0.0)
        bias_masked = np.where(np.abs(bias) - bias_threshold > 0.0, bias, 0.0)
        x_linear = x_masked * sympy.Matrix(weight_masked) + sympy.Matrix([list(bias_masked)])

        if layer_idx < num_hidden_layers:
            unary_ops = operators[layer_idx][0]
            binary_ops = operators[layer_idx][1]
            num_unary = int(num_operators[layer_idx][0])
            num_binary = int(num_operators[layer_idx][1])
        else:
            unary_ops = ["identity"]
            binary_ops = []
            num_unary = int(output_dim)
            num_binary = 0

        unary_aux = np.asarray(layer.aux_unary.numpy(), dtype=np.float64)
        unary_threshold = np.asarray(layer.aux_unary_t.numpy(), dtype=np.float64)
        unary_mask = np.where(unary_aux - unary_threshold > 0.0, 1.0, 0.0)

        if num_binary > 0 and hasattr(layer, "aux_binary"):
            binary_aux = np.asarray(layer.aux_binary.numpy(), dtype=np.float64)
            binary_threshold = np.asarray(layer.aux_binary_t.numpy(), dtype=np.float64)
            binary_mask = np.where(binary_aux - binary_threshold > 0.0, 1.0, 0.0)
        else:
            binary_mask = np.zeros((0,), dtype=np.float64)

        y_masked = sympy.zeros(1, num_unary + num_binary)
        for idx in range(num_unary):
            col = x_linear[0, idx]
            unary_active = float(unary_mask[idx]) if idx < len(unary_mask) else 1.0
            unary_op = unary_ops[idx % len(unary_ops)]
            if unary_active > 0.5:
                y_masked[0, idx] = _math_operation_sympy(unary_op, col)
            else:
                y_masked[0, idx] = _math_operation_sympy("identity", col)

        for idx in range(num_binary):
            left = x_linear[0, num_unary + 2 * idx]
            right = x_linear[0, num_unary + 2 * idx + 1]
            binary_active = float(binary_mask[idx]) if idx < len(binary_mask) else 0.0
            binary_op = binary_ops[idx % len(binary_ops)] if binary_ops else "+"
            if binary_active > 0.5:
                y_masked[0, num_unary + idx] = _math_operation_sympy(binary_op, left, right)
            else:
                y_masked[0, num_unary + idx] = _math_operation_sympy("+", left, right)

        x_masked = y_masked

    rows: list[dict[str, Any]] = []
    for class_idx in range(int(output_dim)):
        expr = x_masked[0, class_idx] if class_idx < x_masked.shape[1] else sympy.Integer(0)
        complexity = int(sum(1 for _ in sympy.preorder_traversal(expr)))
        expr_full = str(expr)
        display_expr = str(sympy.N(expr, significant_digits))
        if not expr.free_symbols:
            expr_full = "N/A (零或常数)"
            display_expr = "N/A"
            complexity = 0
        auc_value = float(class_auc.get(class_idx, float("nan")))
        rows.append(
            {
                "类别": int(class_idx),
                "表达式": display_expr,
                "复杂度": int(complexity),
                "AUC": round(auc_value, 4) if math.isfinite(auc_value) else float("nan"),
                "expr_full": expr_full,
            }
        )
    return rows


def _write_symbolic_summary_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ["类别", "表达式", "复杂度", "AUC", "expr_full"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_roc_auc_summary_csv(path: Path, class_auc: dict[int, float]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["class", "auc"])
        writer.writeheader()
        for class_idx in sorted(class_auc.keys()):
            writer.writerow({"class": int(class_idx), "auc": float(class_auc[class_idx])})


@dataclass
class SymbolNetRunnerConfig:
    output_dir: str = DEFAULT_SYMBOLNET_RUNS_DIR
    seeds: str = "42"
    classes: str = "0,1,2,3,4,5,6,7,8,9"
    max_train_samples: Optional[int] = None
    max_test_samples: Optional[int] = None
    epochs: int = 30
    batch_size: int = 256
    learning_rate: float = 0.005
    num_hidden_layers: int = 1
    unary_ops_csv: str = "sin,cos,exp,gauss"
    binary_ops_csv: str = "*"
    num_unary: int = 20
    num_binary: int = 5
    alpha_sparsity_input: float = 0.95
    alpha_sparsity_model: float = 0.99
    alpha_sparsity_unary: float = 0.4
    alpha_sparsity_binary: float = 0.4
    enable_cnn_boost: bool = False
    cnn_feature_dim: int = 20
    cnn_epochs: int = 6
    cnn_batch_size: int = 256
    cnn_learning_rate: float = 0.001
    quiet: bool = False
    config_path: Optional[str] = None

    unary_ops: list[str] = None  # type: ignore[assignment]
    binary_ops: list[str] = None  # type: ignore[assignment]

    def normalize(self) -> None:
        self.unary_ops = _parse_csv_strs(self.unary_ops_csv)
        self.binary_ops = _parse_csv_strs(self.binary_ops_csv)
        if self.num_hidden_layers < 1:
            raise ValueError("--num-hidden-layers must be >= 1")
        if self.num_unary < 1:
            raise ValueError("--num-unary must be >= 1")
        if self.num_binary < 0:
            raise ValueError("--num-binary must be >= 0")
        if self.epochs < 1:
            raise ValueError("--epochs must be >= 1")
        if self.batch_size < 1:
            raise ValueError("--batch-size must be >= 1")
        if self.learning_rate <= 0.0:
            raise ValueError("--learning-rate must be > 0")
        if self.cnn_feature_dim < 1:
            raise ValueError("--cnn-feature-dim must be >= 1")
        if self.cnn_epochs < 1:
            raise ValueError("--cnn-epochs must be >= 1")
        if self.cnn_batch_size < 1:
            raise ValueError("--cnn-batch-size must be >= 1")
        if self.cnn_learning_rate <= 0.0:
            raise ValueError("--cnn-learning-rate must be > 0")


class SymbolNetConfigError(ValueError):
    """Raised when symbolnet yaml template is invalid or incompatible."""


def _as_mapping(value: Any, context: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise SymbolNetConfigError(f"{context} must be a mapping")
    return value


def _coerce_csv_like(value: Any, field_name: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    raise SymbolNetConfigError(f"{field_name} must be a string or list")


def _resolve_config_path(raw: Optional[str], repo_root: Path) -> Path:
    if raw is None:
        return (repo_root / DEFAULT_SYMBOLNET_CONFIG_PATH).resolve()
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root / candidate).resolve()


def load_symbolnet_runner_config(config_path: Path) -> SymbolNetRunnerConfig:
    import yaml

    if not config_path.exists():
        raise FileNotFoundError(f"symbolnet config not found: {config_path}")

    payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    root = _as_mapping(payload, "config root")

    allowed_root = {"template", "run", "data", "model", "sparsity"}
    unknown_root = sorted(set(root.keys()) - allowed_root)
    if unknown_root:
        raise SymbolNetConfigError(f"unknown symbolnet config sections: {unknown_root}")

    template = _as_mapping(root.get("template"), "template")
    if str(template.get("kind", "")).strip() != "symbolnet":
        raise SymbolNetConfigError("template.kind must be 'symbolnet'")
    if int(template.get("version", -1)) != 1:
        raise SymbolNetConfigError("template.version must be 1")

    cfg = SymbolNetRunnerConfig()
    cfg.config_path = str(config_path)

    run = _as_mapping(root.get("run"), "run")
    data = _as_mapping(root.get("data"), "data")
    model = _as_mapping(root.get("model"), "model")
    sparsity = _as_mapping(root.get("sparsity"), "sparsity")

    allowed_run = {"output_dir", "seeds", "quiet"}
    allowed_data = {
        "classes",
        "max_train_samples",
        "max_test_samples",
        "enable_cnn_boost",
        "cnn_feature_dim",
        "cnn_epochs",
        "cnn_batch_size",
        "cnn_learning_rate",
    }
    allowed_model = {
        "epochs",
        "batch_size",
        "learning_rate",
        "num_hidden_layers",
        "unary_ops",
        "binary_ops",
        "num_unary",
        "num_binary",
    }
    allowed_sparsity = {
        "alpha_sparsity_input",
        "alpha_sparsity_model",
        "alpha_sparsity_unary",
        "alpha_sparsity_binary",
    }

    unknown = sorted(set(run.keys()) - allowed_run)
    if unknown:
        raise SymbolNetConfigError(f"unknown run keys: {unknown}")
    unknown = sorted(set(data.keys()) - allowed_data)
    if unknown:
        raise SymbolNetConfigError(f"unknown data keys: {unknown}")
    unknown = sorted(set(model.keys()) - allowed_model)
    if unknown:
        raise SymbolNetConfigError(f"unknown model keys: {unknown}")
    unknown = sorted(set(sparsity.keys()) - allowed_sparsity)
    if unknown:
        raise SymbolNetConfigError(f"unknown sparsity keys: {unknown}")

    if "output_dir" in run:
        cfg.output_dir = str(run["output_dir"])
    if "seeds" in run:
        cfg.seeds = _coerce_csv_like(run["seeds"], "run.seeds")
    if "quiet" in run:
        cfg.quiet = bool(run["quiet"])

    if "classes" in data:
        cfg.classes = _coerce_csv_like(data["classes"], "data.classes")
    if "max_train_samples" in data:
        cfg.max_train_samples = None if data["max_train_samples"] is None else int(data["max_train_samples"])
    if "max_test_samples" in data:
        cfg.max_test_samples = None if data["max_test_samples"] is None else int(data["max_test_samples"])
    if "enable_cnn_boost" in data:
        cfg.enable_cnn_boost = bool(data["enable_cnn_boost"])
    if "cnn_feature_dim" in data:
        cfg.cnn_feature_dim = int(data["cnn_feature_dim"])
    if "cnn_epochs" in data:
        cfg.cnn_epochs = int(data["cnn_epochs"])
    if "cnn_batch_size" in data:
        cfg.cnn_batch_size = int(data["cnn_batch_size"])
    if "cnn_learning_rate" in data:
        cfg.cnn_learning_rate = float(data["cnn_learning_rate"])

    if "epochs" in model:
        cfg.epochs = int(model["epochs"])
    if "batch_size" in model:
        cfg.batch_size = int(model["batch_size"])
    if "learning_rate" in model:
        cfg.learning_rate = float(model["learning_rate"])
    if "num_hidden_layers" in model:
        cfg.num_hidden_layers = int(model["num_hidden_layers"])
    if "unary_ops" in model:
        cfg.unary_ops_csv = _coerce_csv_like(model["unary_ops"], "model.unary_ops")
    if "binary_ops" in model:
        cfg.binary_ops_csv = _coerce_csv_like(model["binary_ops"], "model.binary_ops")
    if "num_unary" in model:
        cfg.num_unary = int(model["num_unary"])
    if "num_binary" in model:
        cfg.num_binary = int(model["num_binary"])

    if "alpha_sparsity_input" in sparsity:
        cfg.alpha_sparsity_input = float(sparsity["alpha_sparsity_input"])
    if "alpha_sparsity_model" in sparsity:
        cfg.alpha_sparsity_model = float(sparsity["alpha_sparsity_model"])
    if "alpha_sparsity_unary" in sparsity:
        cfg.alpha_sparsity_unary = float(sparsity["alpha_sparsity_unary"])
    if "alpha_sparsity_binary" in sparsity:
        cfg.alpha_sparsity_binary = float(sparsity["alpha_sparsity_binary"])

    cfg.normalize()
    return cfg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SymbolNet runner for MNIST benchmark-style comparisons.")
    parser.add_argument("--config", default=None, help="symbolnet yaml config path (default: configs/symbolnet/symbolnet.default.yaml)")
    parser.add_argument("--output-dir", default=None, help="output directory")
    parser.add_argument("--seeds", default=None, help="comma-separated random seeds")
    parser.add_argument("--classes", default=None, help="comma-separated MNIST classes")
    parser.add_argument("--max-train-samples", type=int, default=None, help="optional train subset size")
    parser.add_argument("--max-test-samples", type=int, default=None, help="optional test subset size")
    parser.add_argument("--cnn-boost", action=argparse.BooleanOptionalAction, default=None, help="enable optional CNN feature boost before SymbolNet training")
    parser.add_argument("--cnn-feature-dim", type=int, default=None, help="feature dimension used by CNN boost")
    parser.add_argument("--cnn-epochs", type=int, default=None, help="CNN boost training epochs")
    parser.add_argument("--cnn-batch-size", type=int, default=None, help="CNN boost batch size")
    parser.add_argument("--cnn-learning-rate", type=float, default=None, help="CNN boost learning rate")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--num-hidden-layers", type=int, default=None)
    parser.add_argument("--unary-ops", default=None, help="comma-separated unary operators")
    parser.add_argument("--binary-ops", default=None, help="comma-separated binary operators")
    parser.add_argument("--num-unary", type=int, default=None)
    parser.add_argument("--num-binary", type=int, default=None)
    parser.add_argument("--alpha-sparsity-input", type=float, default=None)
    parser.add_argument("--alpha-sparsity-model", type=float, default=None)
    parser.add_argument("--alpha-sparsity-unary", type=float, default=None)
    parser.add_argument("--alpha-sparsity-binary", type=float, default=None)
    parser.add_argument("--quiet", action=argparse.BooleanOptionalAction, default=None, help="silence per-epoch fit logs")
    return parser


def parse_symbolnet_cli_config(argv: Optional[list[str]] = None) -> SymbolNetRunnerConfig:
    repo_root = Path(__file__).resolve().parents[1]
    parser = build_parser()
    namespace = parser.parse_args(argv)
    config_path = _resolve_config_path(namespace.config, repo_root)
    cfg = load_symbolnet_runner_config(config_path)

    cfg.config_path = str(config_path)
    if namespace.output_dir is not None:
        cfg.output_dir = namespace.output_dir
    if namespace.seeds is not None:
        cfg.seeds = namespace.seeds
    if namespace.classes is not None:
        cfg.classes = namespace.classes
    if namespace.max_train_samples is not None:
        cfg.max_train_samples = namespace.max_train_samples
    if namespace.max_test_samples is not None:
        cfg.max_test_samples = namespace.max_test_samples
    if namespace.cnn_boost is not None:
        cfg.enable_cnn_boost = bool(namespace.cnn_boost)
    if namespace.cnn_feature_dim is not None:
        cfg.cnn_feature_dim = namespace.cnn_feature_dim
    if namespace.cnn_epochs is not None:
        cfg.cnn_epochs = namespace.cnn_epochs
    if namespace.cnn_batch_size is not None:
        cfg.cnn_batch_size = namespace.cnn_batch_size
    if namespace.cnn_learning_rate is not None:
        cfg.cnn_learning_rate = namespace.cnn_learning_rate
    if namespace.epochs is not None:
        cfg.epochs = namespace.epochs
    if namespace.batch_size is not None:
        cfg.batch_size = namespace.batch_size
    if namespace.learning_rate is not None:
        cfg.learning_rate = namespace.learning_rate
    if namespace.num_hidden_layers is not None:
        cfg.num_hidden_layers = namespace.num_hidden_layers
    if namespace.unary_ops is not None:
        cfg.unary_ops_csv = namespace.unary_ops
    if namespace.binary_ops is not None:
        cfg.binary_ops_csv = namespace.binary_ops
    if namespace.num_unary is not None:
        cfg.num_unary = namespace.num_unary
    if namespace.num_binary is not None:
        cfg.num_binary = namespace.num_binary
    if namespace.alpha_sparsity_input is not None:
        cfg.alpha_sparsity_input = namespace.alpha_sparsity_input
    if namespace.alpha_sparsity_model is not None:
        cfg.alpha_sparsity_model = namespace.alpha_sparsity_model
    if namespace.alpha_sparsity_unary is not None:
        cfg.alpha_sparsity_unary = namespace.alpha_sparsity_unary
    if namespace.alpha_sparsity_binary is not None:
        cfg.alpha_sparsity_binary = namespace.alpha_sparsity_binary
    if namespace.quiet is not None:
        cfg.quiet = bool(namespace.quiet)

    cfg.normalize()
    return cfg


def _apply_cnn_boost_stability_params(runner: SymbolNetRunnerConfig) -> dict[str, tuple[Any, Any]]:
    if not runner.enable_cnn_boost:
        return {}

    updates: dict[str, tuple[Any, Any]] = {}

    if runner.learning_rate != CNN_BOOST_STABLE_LEARNING_RATE:
        updates["learning_rate"] = (runner.learning_rate, CNN_BOOST_STABLE_LEARNING_RATE)
        runner.learning_rate = CNN_BOOST_STABLE_LEARNING_RATE
    unary_ops_current = _parse_csv_strs(runner.unary_ops_csv)
    has_forbidden_unary = any(op in CNN_BOOST_FORBIDDEN_UNARY_OPS for op in unary_ops_current)
    if has_forbidden_unary or runner.unary_ops_csv != CNN_BOOST_STABLE_UNARY_OPS_CSV:
        updates["unary_ops_csv"] = (runner.unary_ops_csv, CNN_BOOST_STABLE_UNARY_OPS_CSV)
        runner.unary_ops_csv = CNN_BOOST_STABLE_UNARY_OPS_CSV
    if runner.alpha_sparsity_input != CNN_BOOST_STABLE_ALPHA_SPARSITY_INPUT:
        updates["alpha_sparsity_input"] = (runner.alpha_sparsity_input, CNN_BOOST_STABLE_ALPHA_SPARSITY_INPUT)
        runner.alpha_sparsity_input = CNN_BOOST_STABLE_ALPHA_SPARSITY_INPUT
    if runner.alpha_sparsity_model != CNN_BOOST_STABLE_ALPHA_SPARSITY_MODEL:
        updates["alpha_sparsity_model"] = (runner.alpha_sparsity_model, CNN_BOOST_STABLE_ALPHA_SPARSITY_MODEL)
        runner.alpha_sparsity_model = CNN_BOOST_STABLE_ALPHA_SPARSITY_MODEL

    if updates:
        runner.normalize()
    return updates


def run_symbolnet(runner: SymbolNetRunnerConfig) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = _resolve_output_dir(runner.output_dir, repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    classes = sorted(set(_parse_csv_ints(runner.classes, "--classes")))
    seeds = _parse_csv_ints(runner.seeds, "--seeds")
    dataset = load_mnist_data(classes, runner.max_train_samples, runner.max_test_samples)
    if runner.enable_cnn_boost:
        stability_updates = _apply_cnn_boost_stability_params(runner)
        cnn_seed = seeds[0] if seeds else 42
        dataset = _apply_cnn_boost(
            dataset,
            feature_dim=runner.cnn_feature_dim,
            epochs=runner.cnn_epochs,
            batch_size=runner.cnn_batch_size,
            learning_rate=runner.cnn_learning_rate,
            seed=cnn_seed,
            quiet=runner.quiet,
        )
        print(
            f"[symbolnet] cnn boost enabled: raw_input_dim={dataset.get('raw_input_dim', '?')} "
            f"-> input_dim={dataset['input_dim']} (feature_dim={runner.cnn_feature_dim})"
        )
        if stability_updates:
            print(
                "[symbolnet] cnn boost stability params applied: "
                f"learning_rate={runner.learning_rate}, "
                f"unary_ops={runner.unary_ops}, "
                f"alpha_sparsity_input={runner.alpha_sparsity_input}, "
                f"alpha_sparsity_model={runner.alpha_sparsity_model}"
            )

    summary_rows: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds, start=1):
        run_dir = output_dir / f"run_{index:02d}_seed{seed}"
        run_dir.mkdir(parents=True, exist_ok=True)

        run_start = time.perf_counter()
        result = train_symbolnet_once(runner, dataset, seed=seed)
        run_total_seconds = float(time.perf_counter() - run_start)

        metrics_payload = {
            "seed": int(seed),
            "classes": classes,
            "dataset_source": dataset["source"],
            "input_dim": int(dataset["input_dim"]),
            "raw_input_dim": int(dataset.get("raw_input_dim", dataset["input_dim"])),
            "output_dim": int(dataset["output_dim"]),
            "enable_cnn_boost": bool(runner.enable_cnn_boost),
            "cnn_feature_dim": int(runner.cnn_feature_dim),
            "cnn_epochs": int(runner.cnn_epochs),
            "cnn_batch_size": int(runner.cnn_batch_size),
            "cnn_learning_rate": float(runner.cnn_learning_rate),
            "epochs": int(runner.epochs),
            "batch_size": int(runner.batch_size),
            "learning_rate": float(runner.learning_rate),
            "num_hidden_layers": int(runner.num_hidden_layers),
            "unary_ops": list(runner.unary_ops),
            "binary_ops": list(runner.binary_ops),
            "num_unary": int(runner.num_unary),
            "num_binary": int(runner.num_binary),
            "alpha_sparsity_input": float(runner.alpha_sparsity_input),
            "alpha_sparsity_model": float(runner.alpha_sparsity_model),
            "alpha_sparsity_unary": float(runner.alpha_sparsity_unary),
            "alpha_sparsity_binary": float(runner.alpha_sparsity_binary),
            "accuracy": float(result["accuracy"]),
            "macro_auc_ovr": float(result["macro_auc_ovr"]),
            "train_seconds": float(result["train_seconds"]),
            "seed_train_wall_time_s": float(result["train_seconds"]),
            "predict_seconds": float(result["predict_seconds"]),
            "run_total_seconds": run_total_seconds,
            "samples_train": int(result["samples_train"]),
            "samples_test": int(result["samples_test"]),
        }
        _write_metrics_json(run_dir / "metrics.json", metrics_payload)
        _write_history_csv(run_dir / "history.csv", result["history"])
        _write_roc_auc_summary_csv(run_dir / "roc_auc_summary.csv", result["class_auc"])
        symbolic_rows = _build_symbolic_summary_rows(
            model=result["symbolic_model"],
            model_dim=result["model_dim"],
            operators=result["operators"],
            num_operators=result["num_operators"],
            class_auc=result["class_auc"],
        )
        _write_symbolic_summary_csv(run_dir / "symbolnet_symbolic_summary.csv", symbolic_rows)

        summary_row = {"run_index": int(index), **metrics_payload, "run_dir": str(run_dir)}
        summary_rows.append(summary_row)
        print(
            f"[symbolnet] run {index}/{len(seeds)} seed={seed} "
            f"accuracy={metrics_payload['accuracy']:.4f} auc={metrics_payload['macro_auc_ovr']:.4f}"
        )

    summary_path = output_dir / "symbolnet_runs.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        columns = list(summary_rows[0].keys()) if summary_rows else ["run_index"]
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"[symbolnet] completed {len(summary_rows)} run(s)")
    print(f"[symbolnet] output_dir = {output_dir}")


def main() -> None:
    runner = parse_symbolnet_cli_config()
    run_symbolnet(runner)


if __name__ == "__main__":
    main()
