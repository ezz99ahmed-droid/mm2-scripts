# MM2 Scripts — Architecture

Plugin host with four extension points:

- `esp_overlay` — draws boxes, gated by `RoundState.scripts_armed`
- `aimbot_core` — FOV-limited lock with smoothing
- `auto_farm` — coin walker, emits Lua inject payloads
- `skin_inject` — resolves cosmetic names via `mm2_core.skin_engine`

Host flow: `HostBootstrap.boot()` -> `ExtensionLoader.discover()` ->
`PluginRegistry.register()` -> extension `on_load(ctx)`.

Injections travel to `executor/Program.cs` over `\\.\pipe\mm2_executor`.