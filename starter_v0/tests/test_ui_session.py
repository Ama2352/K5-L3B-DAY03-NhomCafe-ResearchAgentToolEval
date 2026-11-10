import json

from providers.base import ModelResponse, ToolCall


class ScriptedProvider:
    default_model = "offline-test"

    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []

    def complete(self, messages, tools=None, **kwargs):
        self.messages.append(messages)
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def new_session(tmp_path, provider):
    from ui_session import ChatSession
    prompt = tmp_path / "prompt.md"
    tools = tmp_path / "tools.yaml"
    prompt.write_text("Original instructions", encoding="utf-8")
    tools.write_text("tools: []", encoding="utf-8")
    return ChatSession(provider=provider, provider_name="fake", model=None,
                       version="test", prompt_path=prompt, tools_path=tools,
                       transcripts_dir=tmp_path / "transcripts")


def test_session_keeps_original_artifacts_when_cp2_changes_files(tmp_path):
    provider = ScriptedProvider([ModelResponse(text="ok")])
    session = new_session(tmp_path, provider)
    original_hash = session.transcript["prompt_hash"]
    (tmp_path / "prompt.md").write_text("Changed by CP2", encoding="utf-8")
    (tmp_path / "tools.yaml").write_text("invalid yaml: [", encoding="utf-8")
    session.submit("Hello")
    assert provider.messages[0][0]["content"] == "Original instructions"
    stored = json.loads(session.path.read_text(encoding="utf-8"))
    assert stored["prompt_hash"] == original_hash
    assert stored["prompt_snapshot"] == "Original instructions"
    assert stored["tool_declarations"] == []


def test_clarification_and_followup_share_history_and_save_tool_records(tmp_path):
    provider = ScriptedProvider([
        ModelResponse(tool_calls=[ToolCall("clarify", {"question": "Tài khoản nào?"})]),
        ModelResponse(text="Đã nhận tài khoản."),
    ])
    session = new_session(tmp_path, provider)
    first = session.submit("Xem bài đăng")
    assert first["status"] == "waiting_for_user"
    assert first["tool_events"][0]["result"]["awaiting_user"] is True
    session.submit("sama")
    assert provider.messages[1][1:3] == [
        {"role": "user", "content": "Xem bài đăng"},
        {"role": "assistant", "content": "Tài khoản nào?"},
    ]
    assert len(json.loads(session.path.read_text(encoding="utf-8"))["turns"]) == 2


def test_provider_error_is_preserved_as_failed_turn(tmp_path):
    session = new_session(tmp_path, ScriptedProvider([RuntimeError("provider unavailable")]))
    turn = session.submit("Hello")
    assert turn["status"] == "provider_error"
    assert "provider unavailable" in turn["error"]
    assert session.history == []
    assert json.loads(session.path.read_text(encoding="utf-8"))["turns"][0]["status"] == "provider_error"


def test_new_session_does_not_overwrite_existing_transcript(tmp_path):
    first = new_session(tmp_path, ScriptedProvider([]))
    second = new_session(tmp_path, ScriptedProvider([]))
    assert first.path != second.path
    assert first.path.exists() and second.path.exists()


def test_disk_failure_keeps_completed_turn_in_memory_for_download(tmp_path, monkeypatch):
    import pytest
    import ui_session
    session = new_session(tmp_path, ScriptedProvider([ModelResponse(text="Saved in memory")]))

    def fail_write(*args):
        raise OSError("disk full")

    monkeypatch.setattr(ui_session, "write_transcript", fail_write)
    with pytest.raises(OSError, match="disk full"):
        session.submit("Hello")
    assert session.transcript["turns"][0]["assistant_text"] == "Saved in memory"


def test_send_failure_redacts_token_before_model_and_transcript(tmp_path, monkeypatch, fake_http):
    import requests
    token = "123456:offline-test-bot-secret"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", token)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "offline-chat")
    fake_http(requests.HTTPError(f"403 Forbidden for url: https://api.telegram.org/bot{token}/sendMessage"))
    provider = ScriptedProvider([
        ModelResponse(tool_calls=[ToolCall("send", {"text": "Test", "confirmed": True})]),
        ModelResponse(text="Send failed."),
    ])
    session = new_session(tmp_path, provider)
    turn = session.submit("Confirmed: send Test")
    error = turn["tool_events"][0]["result"]
    assert error["error"] == "HTTPError"
    assert "403" in error["message"]
    assert "[REDACTED]" in error["message"]
    assert token not in json.dumps(turn)
    assert token not in json.dumps(provider.messages)
    assert token not in session.path.read_text(encoding="utf-8")
