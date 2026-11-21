"""YAML config loader with defaults for the mm2 host."""
from __future__ import annotations

from pathlib import Path

import yaml


DEFAULTS = {
    "host": {"log_level": "INFO", "data_dir": "data"},
    "executor": {"pipe": r"\\.\pipe\mm2_executor", "autoload": True},
    "extensions": {"autostart": ["esp_overlay", "aimbot_core"]},
}


def load_config(path: Path) -> dict:
    if not path.exists():
        return DEFAULTS
    with path.open("r", encoding="utf-8") as fh:
        user = yaml.safe_load(fh) or {}
    merged = {**DEFAULTS}
    for section, values in user.items():
        merged[section] = {**DEFAULTS.get(section, {}), **values}
    return merged