"""Minimal CP5 chat UI; execution stays in the existing Python agent."""
from pathlib import Path
import json

import streamlit as st

from providers import make_provider
from ui_session import ChatSession

ROOT = Path(__file__).resolve().parent

STYLES = """<style>
:root {
    color-scheme: light;
    --background: #f3f6f4; --foreground: #20382c; --muted: #f3f6f4;
    --muted-foreground: #506457; --border: #c5d2ca; --primary: #285b46;
}
.stApp, [data-testid="stHeader"], [data-testid="stBottom"] {
    background: var(--background); color: var(--foreground);
}
.stApp, .stApp :is(h1,h2,h3,p,input,textarea,button,label,select) {
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp :is(h1,h2,h3,h4,p,label,summary),
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stWidgetLabel"] {color: var(--foreground);}
.stApp :is(input,textarea),
.stApp [data-baseweb="select"] > div {
    background: var(--background); color: var(--foreground);
    -webkit-text-fill-color: var(--foreground);
}
.stApp :is(input,textarea)::placeholder {
    color: var(--muted-foreground); -webkit-text-fill-color: var(--muted-foreground); opacity: 1;
}
.stApp [data-testid="stCaptionContainer"] p {color: var(--muted-foreground);}
.stApp :is(input,textarea):disabled {opacity: 1; color: var(--muted-foreground);}
[data-testid="stMainBlockContainer"] {max-width: 820px; padding: 2.5rem 2rem 6rem;}
[data-testid="stSidebar"] {background: var(--muted); border-right: 1px solid var(--border);}
[data-testid="stSidebarContent"] {padding-top: 1rem;}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {gap: 1rem;}
.brand {font-size: 1.35rem; font-weight: 650; letter-spacing: -.045em; margin: 0;}
.brand-note {font-size: .82rem; color: var(--muted-foreground); margin: .2rem 0 1.1rem;}
.welcome {text-align: center; margin: clamp(3rem, 15vh, 8rem) auto 1.8rem;}
.welcome h1 {
    font-size: clamp(1.8rem, 4vw, 2.4rem); font-weight: 600;
    letter-spacing: -.045em; line-height: 1.25; color: var(--foreground); padding-bottom: .8rem;
}
.welcome p {font-size: .98rem; line-height: 1.65; color: var(--muted-foreground);}
.conversation-title {font-size: .85rem; color: var(--muted-foreground); margin-bottom: 2rem;}
.stApp :is(button,input):focus-visible {outline: 2px solid var(--primary); outline-offset: 3px;}
.stApp [data-testid="stBaseButton-secondary"] {
    background: var(--background); color: var(--foreground);
    border-color: var(--border); border-radius: 8px; box-shadow: none;
}
.stApp [data-testid="stBaseButton-secondary"]:hover {border-color: var(--primary); color: var(--primary);}
[data-testid="stChatMessage"] {background: none; border: none; padding: 1rem 0;}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--muted); border-radius: 12px; padding: .75rem 1rem;
    margin-left: auto; width: fit-content; max-width: 90%;
}
[data-testid="stChatMessageAvatarUser"] {display: none;}
[data-testid="stChatMessageAvatarAssistant"] {background: var(--muted); color: var(--primary);}
.stApp [data-testid="stChatInput"] {
    background: var(--background); border: 1px solid var(--border);
    border-radius: 14px; box-shadow: 0 3px 18px #202b2608;
}
.stApp [data-testid="stChatInput"]:focus-within {border-color: var(--primary);}
.stApp [data-testid="stChatInput"] > div {border: none; background: transparent; box-shadow: none;}
.stApp [data-testid="stChatInput"] textarea:focus-visible {outline: none;}
[data-testid="stChatInput"] textarea {font-size: .95rem;}
[data-testid="stChatInputSubmitButton"] {color: var(--primary);}
.stApp [data-testid="stExpander"] {border-color: var(--border); border-radius: 8px;}
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] {padding: 1.5rem 1rem 5rem;}
    .welcome {margin-top: 3rem;}
}
@media (prefers-reduced-motion: reduce) {
    .stApp *, .stApp *::before, .stApp *::after {animation: none !important; transition: none !important;}
}
</style>"""


def render_turn(turn):
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant", avatar=":material/manage_search:"):
        if turn.get("error"):
            st.error("Không nhận được phản hồi. Kiểm tra kết nối hoặc nhà cung cấp trong Cài đặt rồi thử lại.")
            st.caption(turn["error"])
        if turn.get("assistant_text"):
            st.markdown(turn["assistant_text"])
        if turn["status"] == "waiting_for_user":
            st.caption("Trả lời ở ô chat bên dưới để tiếp tục.")
        elif turn["status"] == "max_tool_rounds":
            st.warning("Đã đạt giới hạn xử lý. Xem hoạt động bên dưới để biết kết quả từng bước.")
        events = turn.get("tool_events", [])
        for event in events:
            result = event.get("result", {})
            if isinstance(result, dict) and result.get("error"):
                st.error(f"Tool {event['tool']}: {result['error']} — {result.get('message', '')}")
        if turn.get("rounds"):
            with st.expander(f"Xem hoạt động ({len(events)} lần gọi công cụ)"):
                st.json(turn["rounds"])


def suggest(text):
    st.session_state["composer"] = text


def main():
    st.set_page_config(page_title="Café Research", page_icon="☕", layout="centered")
    st.markdown(STYLES, unsafe_allow_html=True)
    session = st.session_state.get("research_session")

    with st.sidebar:
        st.markdown('<p class="brand">Café Research</p><p class="brand-note">Trợ lý nghiên cứu của bạn</p>', unsafe_allow_html=True)
        if st.button("Cuộc trò chuyện mới", key="new_chat", icon=":material/add:", use_container_width=True):
            st.session_state.pop("research_session", None)
            st.session_state.pop("save_error", None)
            st.session_state["composer"] = ""
            session = None

        with st.expander("Cài đặt"):
            provider_name = st.selectbox("Nhà cung cấp", ["openrouter", "deepseek", "openai", "anthropic", "gemini", "ollama"],
                                         key="provider", disabled=session is not None)
            model = st.text_input("Model", placeholder="Mặc định của nhà cung cấp", key="model", disabled=session is not None)
            version = st.text_input("Nhãn phiên bản", value="v0", key="version", disabled=session is not None,
                                    help="Nhãn của prompt/tools hiện tại, không tự tải phiên bản cũ.")
            rounds = st.slider("Số bước xử lý tối đa", 1, 8, 4, key="rounds", disabled=session is not None)
            st.caption("Tạo cuộc trò chuyện mới để đổi cấu hình hoặc nạp prompt/tools mới nhất. API key được cấu hình trong .env trên máy chủ.")

        if session:
            st.caption(f"{session.transcript['provider']} / {session.model}")
            with st.expander("Thông tin phiên"):
                st.caption(f"Phiên bản: {session.transcript['version']}")
                st.code(session.transcript["artifact_version"], language=None)
                st.caption(f"{len(session.transcript['turns'])} lượt trò chuyện. Tự lưu sau mỗi lượt.")
                st.caption(session.path.name)
            st.download_button("Tải transcript JSON", json.dumps(session.transcript, ensure_ascii=False, indent=2),
                               file_name=session.path.name, mime="application/json", use_container_width=True)

    if session and session.transcript["turns"]:
        st.markdown('<p class="conversation-title">Cuộc trò chuyện</p>', unsafe_allow_html=True)
        for turn in session.transcript["turns"]:
            render_turn(turn)
    else:
        st.markdown('<div class="welcome"><h1>Bạn đang tìm hiểu điều gì?</h1>'
                    '<p>Tìm thông tin, đọc nguồn và tổng hợp điều bạn cần.<br>Bắt đầu bằng một câu hỏi hoặc một đường link.</p></div>',
                    unsafe_allow_html=True)
        left, right = st.columns(2)
        left.button("Tìm tin mới", icon=":material/search:", use_container_width=True,
                    on_click=suggest, args=("Tìm 3 tin tức AI trong tuần này, kèm link nguồn.",))
        right.button("Thử đếm từ", icon=":material/short_text:", use_container_width=True,
                     on_click=suggest, args=("Đếm số từ trong đoạn: Research agents use tools.",))

    if st.session_state.get("save_error"):
        st.error(st.session_state["save_error"])

    user_text = st.chat_input("Hỏi một câu hoặc dán đường link…", key="composer")
    if user_text and user_text.strip():
        if session is None:
            try:
                session = ChatSession(
                    provider=make_provider(provider_name), provider_name=provider_name,
                    model=model.strip() or None, version=version.strip(),
                    prompt_path=ROOT / "artifacts/system_prompt.md",
                    tools_path=ROOT / "artifacts/tools.yaml", transcripts_dir=ROOT / "transcripts",
                    max_tool_rounds=rounds,
                )
                st.session_state["research_session"] = session
            except Exception as exc:
                st.error(f"Không thể bắt đầu trò chuyện: {type(exc).__name__}: {exc}")
                st.caption("Kiểm tra API key và nhà cung cấp trong Cài đặt rồi gửi lại câu hỏi.")
                st.stop()
        with st.spinner("Đang tìm câu trả lời…"):
            try:
                session.submit(user_text)
                st.session_state.pop("save_error", None)
            except OSError as exc:
                st.session_state["save_error"] = f"Không lưu được transcript: {exc}. Bạn vẫn có thể tải JSON ở thanh bên."
        st.rerun()


if __name__ == "__main__":
    main()
