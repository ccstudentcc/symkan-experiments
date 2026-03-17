"""Structured runtime configuration for symkan scripts."""

from symkan.config.schema import BenchmarkConfigModel, DEFAULT_CONFIG, PYDANTIC_AVAILABLE
from symkan.config.loader import (
    BenchmarkConfigError,
    apply_config_defaults,
    load_benchmark_config,
)

__all__ = [
    "BenchmarkConfigError",
    "BenchmarkConfigModel",
    "DEFAULT_CONFIG",
    "PYDANTIC_AVAILABLE",
    "apply_config_defaults",
    "load_benchmark_config",
]
