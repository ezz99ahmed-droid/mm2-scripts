"""Discovers and instantiates extension modules from the extensions/ dir."""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path

from mm2_host.contracts.plugin import MM2Plugin


@dataclass(slots=True)
class ExtensionSpec:
    slug: str
    path: Path
    module_name: str


class ExtensionLoader:
    def __init__(self, extensions_dir: Path) -> None:
        self.extensions_dir = Path(extensions_dir)

    def discover(self) -> list[ExtensionSpec]:
        specs: list[ExtensionSpec] = []
        if not self.extensions_dir.exists():
            return specs
        for entry in sorted(self.extensions_dir.glob("*/plugin.py")):
            slug = entry.parent.name
            specs.append(ExtensionSpec(slug=slug, path=entry, module_name=f"mm2_ext_{slug}"))
        return specs

    def instantiate(self, spec: ExtensionSpec) -> MM2Plugin:
        module_spec = importlib.util.spec_from_file_location(spec.module_name, spec.path)
        if module_spec is None or module_spec.loader is None:
            raise ImportError(f"cannot load {spec.path}")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        factory = getattr(module, "PLUGIN")
        plugin: MM2Plugin = factory()
        return plugin