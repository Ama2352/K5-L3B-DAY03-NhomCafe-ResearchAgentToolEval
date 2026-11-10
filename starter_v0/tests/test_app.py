"""Offline UI integration; these fixtures are not live-chat lab evidence."""
from pathlib import Path

from providers.base import ModelResponse, ToolCall


def test_ui_chat_shows_clarification_tool_errors_and_provider_failure(tmp_path, monkeypatch):
    from streamlit.testing.v1 import AppTest
    import providers
    import ui_session

    class Provider:
        default_model = "offline-test"

        def __init__(self):
            self.responses = iter([
                ModelResponse(tool_calls=[ToolCall("clarify", {"question": "URL nào?"})]),
                ModelResponse(tool_calls=[ToolCall("word_count", {"text": ""})]),
                ModelResponse(text="Không đếm được văn bản rỗng."),
                RuntimeError("offline simulated provider failure"),
            ])

        def complete(self, *args, **kwargs):
            response = next(self.responses)
            if isinstance(response, Exception):
                raise response
            return response

    monkeypatch.setattr(providers, "make_provider", lambda name: Provider())
    original = ui_session.ChatSession

    def isolated_session(**kwargs):
        kwargs["transcripts_dir"] = tmp_path
        return original(**kwargs)

    monkeypatch.setattr(ui_session, "ChatSession", isolated_session)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    assert not app.exception
    # First question starts a session without a separate setup step.
    assert not app.chat_input[0].disabled
    assert len(list(tmp_path.glob("*.transcript.json"))) == 0
    app.chat_input[0].set_value("Đọc bài viết này").run()
    assert not app.exception
    assert any(item.value == "URL nào?" for item in app.markdown)
    app.chat_input[0].set_value("Đếm văn bản rỗng").run()
    assert any("Tool word_count" in item.value for item in app.error)
    app.chat_input[0].set_value("Tiếp tục").run()
    assert any("offline simulated provider failure" in item.value for item in app.caption)
    assert len(list(tmp_path.glob("*.transcript.json"))) == 1
    assert len(app.session_state["research_session"].transcript["turns"]) == 3
    app.button(key="new_chat").click().run()
    assert not app.exception
    assert "research_session" not in app.session_state
    assert not app.chat_input[0].disabled
    assert len(list(tmp_path.glob("*.transcript.json"))) == 1
