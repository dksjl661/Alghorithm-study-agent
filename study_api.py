#!/usr/bin/env python3
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from learning_system import get_analytics, init_learning_system, process_study_turn

HOST = "127.0.0.1"
PORT = 8001

STATE = init_learning_system()


class StudyHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_json({"ok": True})

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"ok": True})
            return

        if parsed.path == "/analytics":
            self._send_json({"ok": True, "analytics": get_analytics(STATE)})
            return

        self._send_json({"ok": False, "error": "Not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path not in {"/study-turn", "/study-turn/stream"}:
            self._send_json({"ok": False, "error": "Not found"}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            body = json.loads(raw or "{}")
            if not isinstance(body, dict):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            self._send_json({"ok": False, "error": "Invalid JSON"}, status=400)
            return

        message = str(body.get("message", "")).strip()
        session_id = body.get("session_id")

        if parsed.path == "/study-turn/stream":
            self._stream_turn(message=message, session_id=session_id)
            return

        result = process_study_turn(STATE, message=message, session_id=session_id)
        self._send_json({"ok": True, **result})

    def _send_sse_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_sse_event(self, payload: dict) -> None:
        chunk = f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")
        self.wfile.write(chunk)
        self.wfile.flush()

    def _stream_turn(self, message: str, session_id: str | None) -> None:
        self._send_sse_headers()
        try:
            self._send_sse_event({"type": "stream_open"})
            result = process_study_turn(
                STATE,
                message=message,
                session_id=session_id,
                on_event=self._send_sse_event,
            )
            self._send_sse_event({"type": "done", "ok": True, "result": result})
        except Exception as exc:
            self._send_sse_event({"type": "error", "ok": False, "error": str(exc)})
        finally:
            self.close_connection = True


if __name__ == "__main__":
    class ReusableServer(ThreadingHTTPServer):
        allow_reuse_address = True
    
    server = ReusableServer((HOST, PORT), StudyHandler)
    print(f"Study API running on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
