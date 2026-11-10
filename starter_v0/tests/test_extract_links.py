from tools import TOOL_FUNCTIONS


def test_extract_links_preserves_order_and_url_content():
    extract = TOOL_FUNCTIONS.get("extract_links")
    assert extract is not None, "extract_links must be registered"
    assert extract("[Paper](https://example.org/paper_(AI)?v=2#abstract). "
                   "Also http://example.net/a, again https://example.org/paper_(AI)?v=2#abstract.") == {
        "tool": "extract_links",
        "urls": ["https://example.org/paper_(AI)?v=2#abstract", "http://example.net/a"],
        "count": 2,
    }


def test_extract_links_accepts_text_without_links():
    extract = TOOL_FUNCTIONS.get("extract_links")
    assert extract is not None, "extract_links must be registered"
    assert extract("No links here; ftp://example.org is not HTTP.") == {
        "tool": "extract_links", "urls": [], "count": 0,
    }


def test_extract_links_returns_errors_for_invalid_input():
    extract = TOOL_FUNCTIONS.get("extract_links")
    assert extract is not None, "extract_links must be registered"
    for value in (None, [], 4, "", " \n ", "Read https://[broken"):
        result = extract(value)
        assert result["tool"] == "extract_links"
        assert result["error"]
