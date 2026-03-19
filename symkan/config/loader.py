from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Optional, Type, Union

import yaml
from pydantic import BaseModel, ValidationError

from symkan.config.exceptions import ConfigError
from symkan.config.schema import AppConfig, StagewiseConfig, SymbolizeConfig, TrainConfig

ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::-(.*?))?\}")


def _expand_env_string(value: str) -> str:
    """Expand ``${VAR}`` placeholders inside a scalar string.

    Args:
        value: Raw scalar string that may contain environment placeholders.

    Returns:
        str: Expanded string with all placeholders resolved.

    Raises:
        ConfigError: If a required environment variable is missing and no
            default value is provided.
    """
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
    """Recursively expand environment placeholders in parsed YAML values.

    Args:
        value: Parsed YAML node, which may be a scalar, list, or mapping.

    Returns:
        Any: Value tree with scalar placeholders expanded in place.

    Raises:
        ConfigError: If placeholders are used in mapping keys.
    """
    if isinstance(value, str):
        return _expand_env_string(value)
    if isinstance(value, list):
        return [_expand_env_placeholders(item) for item in value]
    if isinstance(value, dict):
        expanded: dict[Any, Any] = {}
        for key, item in value.items():
            if isinstance(key, str) and ENV_PATTERN.search(key):
                raise ConfigError(
                    "environment placeholders are only allowed in scalar values, "
                    f"not in mapping keys: {key!r}"
                )
            expanded[key] = _expand_env_placeholders(item)
        return expanded
    return value


def preprocess_yaml_text(text: str) -> str:
    """Expand environment placeholders while keeping YAML values scalar-safe.

    Args:
        text: Raw YAML text before validation.

    Returns:
        str: YAML text re-dumped after placeholder expansion. Returns an empty
        string when the original YAML payload is empty.

    Raises:
        ConfigError: If placeholders appear in mapping keys or required
            environment variables are missing.
    """

    payload = yaml.safe_load(text)
    if payload is None:
        return ""
    expanded_payload = _expand_env_placeholders(payload)
    return yaml.safe_dump(expanded_payload, allow_unicode=True, sort_keys=False)


def _format_validation_error(exc: ValidationError, config_path: Optional[Path]) -> str:
    """Convert a Pydantic validation error into a readable multi-line message.

    Args:
        exc: Original validation error raised by Pydantic.
        config_path: Optional config file path used to add file context.

    Returns:
        str: Human-readable error message suitable for ``ConfigError``.
    """
    prefix = f"invalid config file '{config_path}':" if config_path is not None else "invalid config:"
    details: list[str] = []
    for item in exc.errors():
        loc = ".".join(str(part) for part in item.get("loc", ())) or "<root>"
        msg = item.get("msg", "validation error")
        value = item.get("input", "<missing>")
        details.append(f"{loc}: {msg} (input={value!r})")
    return prefix + "\n- " + "\n- ".join(details)


def _validate_model(
    model_class: Type[BaseModel],
    payload: dict[str, Any],
    config_path: Optional[Path] = None,
):
    """Validate a payload against a specific Pydantic config model.

    Args:
        model_class: Target Pydantic model class.
        payload: Raw mapping to validate.
        config_path: Optional config file path for error reporting.

    Returns:
        BaseModel: Validated model instance of ``model_class``.

    Raises:
        ConfigError: If schema validation fails.
    """
    try:
        return model_class.model_validate(payload)
    except ValidationError as exc:
        raise ConfigError(_format_validation_error(exc, config_path)) from exc


def validate_app_config(values: dict[str, Any]) -> AppConfig:
    """Validate a raw mapping as a full AppConfig.

    Args:
        values: Unvalidated config payload, typically from YAML or tests.

    Returns:
        AppConfig: Canonical validated application config.
    """
    return _validate_model(AppConfig, values)


def validate_train_config(values: dict[str, Any]) -> TrainConfig:
    """Validate a raw mapping as a TrainConfig.

    Args:
        values: Unvalidated training config payload.

    Returns:
        TrainConfig: Validated training config instance.
    """
    return _validate_model(TrainConfig, values)


def validate_stagewise_config(values: dict[str, Any]) -> StagewiseConfig:
    """Validate a raw mapping as a StagewiseConfig.

    Args:
        values: Unvalidated stagewise config payload.

    Returns:
        StagewiseConfig: Validated stagewise config instance.
    """
    return _validate_model(StagewiseConfig, values)


def validate_symbolize_config(values: dict[str, Any]) -> SymbolizeConfig:
    """Validate a raw mapping as a SymbolizeConfig.

    Args:
        values: Unvalidated symbolize config payload.

    Returns:
        SymbolizeConfig: Validated symbolize config instance.
    """
    return _validate_model(SymbolizeConfig, values)


def load_config(config_path: Union[str, Path]) -> AppConfig:
    """Load, expand, and validate an AppConfig from YAML.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        AppConfig: Fully validated application config.

    Raises:
        ConfigError: If the file is missing, unreadable, invalid YAML, empty,
            not a mapping, or fails schema validation.
    """
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

    if payload is None:
        raise ConfigError(f"config file is empty: {path}")

    payload = _expand_env_placeholders(payload)
    if not isinstance(payload, dict):
        raise ConfigError(f"config root must be a mapping: {path}")
    return _validate_model(AppConfig, payload, config_path=path)


def load_app_config(config_path: Union[str, Path]) -> AppConfig:
    """Load an AppConfig via the backward-compatible alias.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        AppConfig: Fully validated application config.
    """

    return load_config(config_path)
