"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

clarify_tool = TOOL_FUNCTIONS["clarify"]
format_tool = TOOL_FUNCTIONS["format"]
send_tool = TOOL_FUNCTIONS["send"]
lookup_tool = TOOL_FUNCTIONS["lookup"]
fetch_tool = TOOL_FUNCTIONS["fetch"]
timeline_tool = TOOL_FUNCTIONS["timeline"]
social_search_tool = TOOL_FUNCTIONS["social_search"]
policy_tool = TOOL_FUNCTIONS["policy"]


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = clarify_tool(question="Which topic?", response_type="choice", options=["AI", "Crypto"])

    assert result["options"] == ["AI", "Crypto"]
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "one", "url": "https://a.com/1", "section": "A"},
        {"title": "two", "url": "https://b.com/2", "section": "B"},
        {"title": "three", "url": "https://a.com/3", "section": "A"},
    ]

    markdown = format_tool(items=items, template="sections")["markdown"]

    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    assert markdown.index("one") < markdown.index("three") < markdown.index("## B")


def test_format_thread_numbers_items() -> None:
    items = [{"title": "first", "url": "https://a.com"}, {"title": "second", "url": "https://b.com"}]

    lines = format_tool(items=items, template="thread")["markdown"].split("\n\n")

    assert lines[0].startswith("1/ first")
    assert lines[1].startswith("2/ second")


@pytest.mark.parametrize("items", [None, []])
def test_format_empty_items_does_not_crash(items) -> None:
    result = format_tool(items=items)

    assert result["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="hello", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "test-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "42"
    assert calls[0]["json"]["text"] == "hello"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="hello", confirmed=True)

    assert calls == []
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = lookup_tool(query="ai news", timeframe=None)

    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "ai news"
    assert result["items"] == []


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "Body text",
        "metadata": {"title": "T", "sourceURL": "https://example.com/final"},
    }}))

    result = fetch_tool(url="https://example.com/start")

    assert calls[0]["json"]["url"] == "https://example.com/start"
    item = result["items"][0]
    assert item["title"] == "T"
    assert item["url"] == "https://example.com/final"
    assert item["source"] == "example.com"
    assert item["summary"] == "Body text"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))

    result = fetch_tool(url="https://example.com")

    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    raw = [{"screen_name": "openai", "text": "no id"}] + [
        {"screen_name": "openai", "tweet_id": str(i), "text": f"tweet {i}"} for i in range(1, 7)
    ]
    calls = fake_http(FakeResponse({"timeline": raw}))

    result = timeline_tool(screenname="openai", limit=3)

    assert calls[0]["params"] == {"screenname": "openai"}
    assert [item["url"] for item in result["items"]] == [
        "https://x.com/openai/status/1",
        "https://x.com/openai/status/2",
        "https://x.com/openai/status/3",
    ]


@pytest.mark.parametrize("search_type", ["Top", "Latest"])
def test_social_search_passes_search_type(monkeypatch, fake_http, search_type) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"timeline": []}))

    result = social_search_tool(query="gpt-5", search_type=search_type)

    assert calls[0]["params"] == {"query": "gpt-5", "search_type": search_type}
    assert result["search_type"] == search_type


# ---------------- policy (local knowledge + trust boundary) ----------------

@pytest.mark.parametrize("query", ["", "   "])
def test_policy_empty_query_returns_no_results(query) -> None:
    assert policy_tool(query=query)["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    results = policy_tool(query="data privacy personal information", policy_area="data_privacy", top_k=5)["results"]

    assert results
    assert all(hit["policy_area"] == "data_privacy" for hit in results)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    results = policy_tool(query="injection probe", policy_area="source_citation", top_k=5)["results"]

    probe = next(hit for hit in results if hit["section"] == "Injection probe")
    assert any("viral tweet" in line for line in probe["untrusted_text"])
    assert "viral tweet" not in probe["facts"]


# CP3: citations tool

def test_citations_formats_sources_in_order():
    from tools.citations.tool import citations
    result = citations([{"title": "Paper A", "url": "https://example.com/a"}, {"title": "Paper B", "url": "https://example.org/b"}])
    assert result["references"] == "[1] Paper A — https://example.com/a\n[2] Paper B — https://example.org/b"
    assert result["count"] == 2


def test_citations_rejects_invalid_items():
    from tools.citations.tool import citations
    for items in ([], "not a list", [None], [{"title": "", "url": "https://example.com"}]):
        assert "error" in citations(items)


def test_citations_returns_error_for_invalid_url():
    from tools.citations.tool import citations
    assert "error" in citations([{"title": "Source", "url": "javascript:alert(1)"}])
    assert "error" in citations([{"title": "Source", "url": "http://[invalid"}])


def test_source_domains_deduplicates_hosts():
    from tools.source_domains.tool import source_domains
    assert source_domains(["https://EXAMPLE.com/a", "https://example.com/b", "http://other.org"]) == {"tool": "source_domains", "domains": ["example.com", "other.org"], "count": 2}


def test_source_domains_rejects_bad_input():
    from tools.source_domains.tool import source_domains
    for value in ([], "https://example.com", [None]):
        assert "error" in source_domains(value)


def test_source_domains_reports_invalid_url():
    from tools.source_domains.tool import source_domains
    for value in ("file:///etc/passwd", "https://[broken"):
        assert "error" in source_domains([value])


def test_word_count_counts_unicode_text():
    from tools.word_count.tool import word_count
    result = word_count("Hello world!")
    assert result["word_count"] == 2
    assert result["character_count"] == 12


def test_word_count_rejects_invalid_input():
    from tools.word_count.tool import word_count
    for value in (None, "", "   ", 3):
        assert "error" in word_count(value)


def test_word_count_reports_no_words():
    from tools.word_count.tool import word_count
    assert "error" in word_count("!!!")
