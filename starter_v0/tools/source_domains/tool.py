from urllib.parse import urlsplit


def source_domains(urls):
    if not isinstance(urls, list) or not urls:
        return {"tool": "source_domains", "error": "urls phải là danh sách không rỗng"}
    domains = []
    for url in urls:
        if not isinstance(url, str):
            return {"tool": "source_domains", "error": "Mỗi URL phải là một chuỗi"}
        try:
            parsed = urlsplit(url.strip())
            host = parsed.hostname
            if parsed.scheme not in ("http", "https") or not host:
                raise ValueError("URL không hợp lệ")
        except ValueError:
            return {"tool": "source_domains", "error": "Mỗi URL phải là URL HTTP(S) hợp lệ"}
        if host not in domains:
            domains.append(host)
    return {"tool": "source_domains", "domains": domains, "count": len(domains)}
