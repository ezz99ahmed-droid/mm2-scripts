"""Console entrypoint: `python -m mm2_host.cli boot`."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from rich.console import Console

from mm2_host.bootstrap import HostBootstrap

console = Console()


def main() -> int:
    parser = argparse.ArgumentParser(prog="mm2-host")
    parser.add_argument("command", choices=["boot", "list"], default="boot", nargs="?")
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    host = HostBootstrap(args.root)
    registry = host.boot()

    if args.command == "list":
        for plugin in registry.all():
            console.print(f"[cyan]{plugin.slug}[/] v{plugin.version} -> {', '.join(plugin.provides)}")
    else:
        console.print(f"[green]host ready[/] — {len(registry.all())} extension(s) loaded")

    host.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())