"""Bootstraps the plugin host: loads config, registers builtin extensions, starts the loader."""
from __future__ import annotations

import logging
from pathlib import Path

from mm2_host.contracts.plugin import PluginContext
from mm2_host.loader.extension_loader import ExtensionLoader
from mm2_host.registry.plugin_registry import PluginRegistry

log = logging.getLogger("mm2.host")


class HostBootstrap:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.registry = PluginRegistry()
        self.loader = ExtensionLoader(self.root / "extensions")

    def boot(self) -> PluginRegistry:
        ctx = PluginContext(
            host_version="2026.1.0",
            data_dir=self.root / "data",
            log=log,
        )
        for spec in self.loader.discover():
            try:
                plugin = self.loader.instantiate(spec)
                self.registry.register(plugin, ctx)
                log.info("registered extension %s v%s", plugin.slug, plugin.version)
            except Exception as exc:  # noqa: BLE001
                log.warning("failed to load %s: %s", spec.path, exc)
        return self.registry

    def shutdown(self) -> None:
        for plugin in self.registry.all():
            plugin.on_unload()