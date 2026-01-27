"""Configuration loading and validation."""

import os
import logging
from typing import Any

logger = logging.getLogger(__name__)

# TODO: Add support for environment variable substitution in config values
# e.g., ${DB_PASSWORD} should be replaced with os.environ.get("DB_PASSWORD")


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

    # TODO: Add YAML loading (requires PyYAML dependency)
    # For now, return a minimal default config
    logger.warning("YAML loading not implemented, using defaults")

    return {
        "environments": {},
        "notifications": {
            "enabled": False,
        },
        "health_check": {
            "timeout": 30,
            "retries": 3,
        },
    }


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
