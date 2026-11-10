from urllib.parse import urlsplit


def citations(items):
    """Định dạng tiêu đề và URL nguồn thành danh sách tham khảo đánh số."""
    if not isinstance(items, list) or not items:
        return {"tool": "citations", "error": "items phải là danh sách không rỗng"}
    lines = []
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            return {"tool": "citations", "error": f"Phần tử {index} phải là một đối tượng"}
        title, url = item.get("title"), item.get("url")
        if not isinstance(title, str) or not title.strip() or not isinstance(url, str) or not url.strip():
            return {"tool": "citations", "error": f"Phần tử {index} cần có tiêu đề và URL"}
        try:
            parsed = urlsplit(url.strip())
            valid = parsed.scheme in ("http", "https") and bool(parsed.hostname)
        except ValueError:
            valid = False
        if not valid:
            return {"tool": "citations", "error": f"Phần tử {index} cần có URL HTTP(S) hợp lệ"}
        lines.append(f"[{index}] {title.strip()} — {url.strip()}")
    return {"tool": "citations", "references": "\n".join(lines), "count": len(lines)}
