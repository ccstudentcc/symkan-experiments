from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from symkan.config.exceptions import ConfigError
from symkan.config.schema import AppConfig, StagewiseConfig, SymbolizeConfig, TrainConfig

ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::-(.*?))?\}")


def _expand_env_string(value: str) -> str:
    def replace_env(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        env_value = os.getenv(name)
        if env_value is not None:
            return env_value
        if default is not None:
            return default
        raise ConfigError(f"environment variable '{name}' is required by config")

    return ENV_PATTERN.sub(replace_env, value)


def _expand_env_placeholders(value: Any) -> Any:
    if isinstance(value, str):
        return _expand_env_string(value)
    if isinstance(value, list):
        return [_expand_env_placeholders(item) for item in value]
    if isinstance(value, dict):
        expanded: dict[Any, Any] = {}
        for key, item in value.items():
            expanded_key = _expand_env_string(key) if isinstance(key, str) else key
            expanded[expanded_key] = _expand_env_placeholders(item)
        return expanded
    return value


def preprocess_yaml_text(text: str) -> str:
    """Expand environment variables after YAML parsing so placeholders stay scalar."""

    payload = yaml.safe_load(text)
    if payload is None:
        return ""
    expanded_payload = _expand_env_placeholders(payload)
    return yaml.safe_dump(expanded_payload, allow_unicode=True, sort_keys=False)


def _format_validation_error(exc: ValidationError, config_path: Path | None) -> str:
    prefix = f"invalid config file '{config_path}':" if config_path is not None else "invalid config:"
    details: list[str] = []
    for item in exc.errors():
        loc = ".".join(str(part) for part in item.get("loc", ())) or "<root>"
        msg = item.get("msg", "validation error")
        value = item.get("input", "<missing>")
        details.append(f"{loc}: {msg} (input={value!r})")
    return prefix + "\n- " + "\n- ".join(details)


def _validate_model(model_class: type[BaseModel], payload: dict[str, Any], config_path: Path | None = None):
    try:
        return model_class.model_validate(payload)
    except ValidationError as exc:
        raise ConfigError(_format_validation_error(exc, config_path)) from exc


def validate_app_config(values: dict[str, Any]) -> AppConfig:
    return _validate_model(AppConfig, values)


def validate_train_config(values: dict[str, Any]) -> TrainConfig:
    return _validate_model(TrainConfig, values)


def validate_stagewise_config(values: dict[str, Any]) -> StagewiseConfig:
    return _validate_model(StagewiseConfig, values)


def validate_symbolize_config(values: dict[str, Any]) -> SymbolizeConfig:
    return _validate_model(SymbolizeConfig, values)


def load_config(config_path: str | Path) -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"failed to read config file '{path}': {exc}") from exc

    try:
        payload = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid config file '{path}': failed to parse YAML ({exc})") from exc

    payload = _expand_env_placeholders(payload or {})
    if not isinstance(payload, dict):
        raise ConfigError(f"config root must be a mapping: {path}")
    return _validate_model(AppConfig, payload, config_path=path)


def load_app_config(config_path: str | Path) -> AppConfig:
    """Backward-compatible alias for the previous loader name."""

    return load_config(config_path)
