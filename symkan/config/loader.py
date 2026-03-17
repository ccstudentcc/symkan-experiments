from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Any, Dict, Union

import yaml

from symkan.config.schema import DEFAULT_CONFIG, PYDANTIC_AVAILABLE, SECTION_FIELD_MAP

if PYDANTIC_AVAILABLE:
    from pydantic import ValidationError
    from symkan.config.schema import BenchmarkConfigModel


ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::-(.*?))?\}")


class BenchmarkConfigError(ValueError):
    """Raised when the benchmark configuration is invalid."""


def _expand_env_vars(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        value = os.getenv(name)
        if value is not None:
            return value
        if default is not None:
            return default
        raise BenchmarkConfigError(f"environment variable '{name}' is required by config")

    return ENV_PATTERN.sub(repl, text)


def _normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for section_name, section_value in payload.items():
        if section_name not in SECTION_FIELD_MAP:
            raise BenchmarkConfigError(f"unknown config section: {section_name}")
        if not isinstance(section_value, dict):
            raise BenchmarkConfigError(f"config section '{section_name}' must be a mapping")
        allowed = SECTION_FIELD_MAP[section_name]
        unknown_fields = sorted(set(section_value) - allowed)
        if unknown_fields:
            raise BenchmarkConfigError(
                f"unknown fields in section '{section_name}': {', '.join(unknown_fields)}"
            )
        for key, value in section_value.items():
            alias_key = key
            if section_name == "stagewise" and key == "lamb_schedule":
                alias_key = "stage_lamb_schedule"
            elif section_name == "stagewise" and key == "lr_schedule":
                alias_key = "stage_lr_schedule"
            normalized[alias_key] = value
    return normalized


def load_benchmark_config(config_path: Union[str, Path, None]) -> Dict[str, Any]:
    defaults = dict(DEFAULT_CONFIG)
    if config_path is None:
        return defaults

    path = Path(config_path)
    if not path.exists():
        raise BenchmarkConfigError(f"config file not found: {path}")

    raw_text = path.read_text(encoding="utf-8")
    expanded_text = _expand_env_vars(raw_text)
    payload = yaml.safe_load(expanded_text) or {}
    if not isinstance(payload, dict):
        raise BenchmarkConfigError("config root must be a mapping")
    normalized = _normalize_payload(payload)

    if not PYDANTIC_AVAILABLE:
        raise BenchmarkConfigError(
            "pydantic is required to validate YAML configs; install dependencies from requirements.txt"
        )

    try:
        validated = BenchmarkConfigModel.model_validate(normalized)
    except ValidationError as exc:
        raise BenchmarkConfigError(str(exc)) from exc
    return validated.model_dump()


def apply_config_defaults(parser: argparse.ArgumentParser, config_values: Dict[str, Any]) -> None:
    for action in parser._actions:
        if not action.dest or action.dest == "help":
            continue
        if action.dest not in config_values:
            continue
        if action.default != argparse.SUPPRESS:
            action.default = config_values[action.dest]
