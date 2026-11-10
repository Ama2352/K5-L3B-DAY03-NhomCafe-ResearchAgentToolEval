import re
from urllib.parse import urlsplit


def extract_links(text):
    """Extract unique HTTP(S) links locally, without fetching their targets."""
    if not isinstance(text, str) or not text.strip():
        return {"tool": "extract_links", "error": "text must be a nonempty string"}
    urls = []
    for match in re.finditer(r"https?://[^\s<>\"']*", text, re.IGNORECASE):
        url = match.group().rstrip(".,;:!?")
        # Drop prose/Markdown delimiters, retaining balanced URL parentheses.
        while url and url[-1] in ")]}":
            closer = url[-1]
            opener = {")": "(", "]": "[", "}": "{"}[closer]
            if url.count(closer) <= url.count(opener):
                break
            url = url[:-1].rstrip(".,;:!?")
        try:
            parsed = urlsplit(url)
            if not parsed.hostname or parsed.scheme.lower() not in ("http", "https"):
                raise ValueError("Invalid HTTP(S) URL")
            parsed.port  # Reject malformed ports as well as malformed IPv6 brackets.
        except ValueError:
            return {"tool": "extract_links", "error": "text contains an invalid HTTP(S) URL"}
        if url not in urls:
            urls.append(url)
    return {"tool": "extract_links", "urls": urls, "count": len(urls)}
