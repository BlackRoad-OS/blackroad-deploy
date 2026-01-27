"""Configuration loading and validation."""

import os
import re
import logging
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def _substitute_env_vars(value: Any) -> Any:
    """
    Recursively substitute environment variables in config values.

    Supports ${VAR_NAME} syntax for environment variable substitution.
    """
    if isinstance(value, str):
        pattern = r'\$\{([^}]+)\}'
        matches = re.findall(pattern, value)
        for var_name in matches:
            env_value = os.environ.get(var_name, "")
            value = value.replace(f"${{{var_name}}}", env_value)
        return value
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(item) for item in value]
    return value


def load_config(config_path: str) -> dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config file is invalid
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}")

    if config is None:
        config = {}

    config = _substitute_env_vars(config)

    defaults = {
        "environments": {},
        "notifications": {"enabled": False},
        "health_check": {"timeout": 30, "retries": 3},
    }
    for key, default_value in defaults.items():
        if key not in config:
            config[key] = default_value

    return config


def validate_config(config: dict) -> list[str]:
    """
    Validate configuration and return list of errors.

    Args:
        config: Configuration dictionary to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if "environments" not in config:
        errors.append("Missing 'environments' section")

    for env_name, env_config in config.get("environments", {}).items():
        if "host" not in env_config:
            errors.append(f"Environment '{env_name}' missing 'host'")

        # TODO: Add more comprehensive validation
        # - Validate port numbers are in valid range
        # - Validate SSH key paths exist if specified
        # - Validate notification webhook URLs are valid

    return errors
