"""Runtime registry of loaded MM2 plugins, keyed by slug and capability."""
from __future__ import annotations

from collections import defaultdict

from mm2_host.contracts.plugin import MM2Plugin, PluginContext


class PluginRegistry:
    def __init__(self) -> None:
        self._by_slug: dict[str, MM2Plugin] = {}
        self._by_capability: dict[str, list[MM2Plugin]] = defaultdict(list)

    def register(self, plugin: MM2Plugin, ctx: PluginContext) -> None:
        plugin.on_load(ctx)
        self._by_slug[plugin.slug] = plugin
        for cap in plugin.provides:
            self._by_capability[cap].append(plugin)

    def get(self, slug: str) -> MM2Plugin | None:
        return self._by_slug.get(slug)

    def providers(self, capability: str) -> list[MM2Plugin]:
        return list(self._by_capability.get(capability, ()))

    def dispatch(self, capability: str, event: str, payload: dict) -> list[dict]:
        results = []
        for plugin in self.providers(capability):
            try:
                results.append(plugin.handle(event, payload))
            except Exception:  # noqa: BLE001
                self._by_slug.pop(plugin.slug, None)
        return results

    def all(self) -> list[MM2Plugin]:
        return list(self._by_slug.values())