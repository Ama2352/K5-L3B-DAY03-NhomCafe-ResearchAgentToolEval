"""Per-browser chat state; execution and transcript format follow chat.py."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from chat import now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from tools import to_openai_tools


class ChatSession:
    def __init__(self, *, provider: Any, provider_name: str, model: str | None,
                 version: str, prompt_path: Path, tools_path: Path,
                 transcripts_dir: Path, history_window: int = 5,
                 max_tool_rounds: int = 4):
        if not version.strip():
            raise ValueError("Cần nhập nhãn version của prompt/tools đang dùng.")
        self.provider = provider
        self.model = model or getattr(provider, "default_model", None)
        self.history_window = history_window
        self.max_tool_rounds = max_tool_rounds
        self.history: list[dict[str, str]] = []
        # Hash the very bytes used in this session, never re-read changing files.
        prompt_bytes = prompt_path.read_bytes()
        tools_bytes = tools_path.read_bytes()
        self.system_prompt = prompt_bytes.decode("utf-8")
        declarations = yaml.safe_load(tools_bytes.decode("utf-8"))["tools"]
        self.tools = to_openai_tools(declarations)
        prompt_hash = hashlib.sha256(prompt_bytes).hexdigest()
        tools_hash = hashlib.sha256(tools_bytes).hexdigest()
        transcript_id = f"{safe_slug(version)}_{safe_slug(provider_name)}_ui_{uuid4().hex}"
        self.path = transcripts_dir / f"{transcript_id}.transcript.json"
        self.transcript: dict[str, Any] = {
            "transcript_id": transcript_id, "version": version,
            "artifact_version": f"{version}+p{prompt_hash[:12]}+t{tools_hash[:12]}",
            "prompt_hash": prompt_hash, "tools_hash": tools_hash,
            "provider": provider_name, "model": self.model,
            "system_prompt": str(prompt_path), "tools": str(tools_path),
            "prompt_snapshot": self.system_prompt, "tool_declarations": declarations,
            "interface": "streamlit", "history_window": history_window,
            "max_tool_rounds": max_tool_rounds, "created_at": now_iso(),
            "updated_at": now_iso(), "turns": [],
        }
        write_transcript(self.path, self.transcript)

    def submit(self, user_text: str) -> dict[str, Any]:
        if not user_text.strip():
            raise ValueError("Câu hỏi không được để trống.")
        turn: dict[str, Any] = {
            "turn_index": len(self.transcript["turns"]) + 1,
            "started_at": now_iso(), "user": user_text, "status": "started",
            "assistant_text": None, "rounds": [], "tool_events": [],
        }
        try:
            result = run_model_tool_loop(
                provider=self.provider,
                messages=[{"role": "system", "content": self.system_prompt},
                          *trim_history(self.history, self.history_window),
                          {"role": "user", "content": user_text}],
                tools=self.tools, model=self.model, max_tool_rounds=self.max_tool_rounds,
            )
            turn.update(result)
            self.history.extend([
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": result["assistant_text"]},
            ])
        except Exception as exc:
            turn.update(status="provider_error", error=f"{type(exc).__name__}: {exc}")
        turn["ended_at"] = now_iso()
        self.transcript["turns"].append(turn)
        # A write failure propagates to the UI; the turn remains downloadable in memory.
        write_transcript(self.path, self.transcript)
        return turn
