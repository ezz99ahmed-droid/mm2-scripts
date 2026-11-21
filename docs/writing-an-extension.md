# Writing an MM2 extension

1. Create `extensions/<slug>/plugin.py`.
2. Export `PLUGIN = YourClass` — the loader instantiates it.
3. Implement `slug`, `version`, `provides`, `on_load`, `on_unload`, `handle`.
4. Add the manifest entry to `scripts/manifest.yaml`.

Capabilities are matched by `PluginRegistry.dispatch(capability, event, payload)`.