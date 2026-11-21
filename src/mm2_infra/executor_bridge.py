"""Bridge to the Windows executor process (C# bridge) over a local named pipe."""
from __future__ import annotations

import json
import socket
from pathlib import Path
from typing import Any


class ExecutorBridge:
    def __init__(self, pipe_name: str = r"\\.\pipe\mm2_executor") -> None:
        self.pipe_name = pipe_name
        self._sock: socket.socket | None = None

    def attach(self) -> None:
        # Real bridge talks to executor/bridge.csproj — this is the Python side stub.
        try:
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._sock.connect(Path(self.pipe_name).as_posix())
        except (FileNotFoundError, OSError):
            self._sock = None

    def inject(self, lua_source: str) -> dict[str, Any]:
        if self._sock is None:
            return {"ok": False, "error": "executor not attached"}
        payload = json.dumps({"op": "inject", "src": lua_source}).encode()
        self._sock.sendall(payload)
        return json.loads(self._sock.recv(4096))

    def detach(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None