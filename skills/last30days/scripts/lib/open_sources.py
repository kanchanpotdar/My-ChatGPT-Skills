"""Open, low-authentication research sources.

These adapters deliberately return the small raw-item shape consumed by the
existing normalization layer.  They never raise for network failures; the
pipeline records the HTTP status as a degraded source outcome.
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import time
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import threading
from datetime import datetime, timezone
from typing import Any

from . import log

TIMEOUT = 20
CACHE_TTL = 900
_SEMANTIC_LOCK = threading.Lock()
_SEMANTIC_LAST = 0.0

def _cache_path(url: str) -> Path:
    root = Path(os.environ.get("LAST30DAYS_CACHE_DIR", "/tmp/last30days-cache"))
    root.mkdir(parents=True, exist_ok=True)
    return root / (hashlib.sha256(url.encode()).hexdigest() + ".json")

def _cached(url: str) -> tuple[Any, dict[str, Any]] | None:
    try:
        path = _cache_path(url)
        if time.time() - path.stat().st_mtime > CACHE_TTL:
            return None
        payload = json.loads(path.read_text())
        return payload.get("data"), {"status": payload.get("status", 200), "cached": True}
    except (OSError, ValueError, TypeError):
        return None

def _store_cache(url: str, data: Any, meta: dict[str, Any]) -> None:
    try:
        _cache_path(url).write_text(json.dumps({"data": data, "status": meta.get("status", 200)}))
    except (OSError, TypeError):
        pass

def _get(url: str, headers: dict[str, str] | None = None) -> tuple[Any, dict[str, Any]]:
    cached = _cached(url)
    if cached is not None:
        return cached
    for attempt in range(3):
      try:
        req = urllib.request.Request(url, headers={"User-Agent": "last30days/3.39 (+research bot)", **(headers or {})})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            body = response.read()
            ctype = response.headers.get("content-type", "")
            if "xml" in ctype or url.endswith(".xml") or body.lstrip().startswith(b"<"):
                data = ET.fromstring(body)
            else:
                data = json.loads(body.decode("utf-8"))
            meta = {"status": response.status}
            _store_cache(url, data, meta)
            return data, meta
      except urllib.error.HTTPError as exc:
        if exc.code in {429, 500, 502, 503, 504} and attempt < 2:
            retry_after = exc.headers.get("Retry-After") if exc.headers else None
            try:
                delay = max(2 ** attempt * 2, float(retry_after or 0))
            except ValueError:
                delay = 2 ** attempt * 2
            time.sleep(delay)
            continue
        log.source_log("open-source", f"request failed: {exc}", tty_only=False)
        return [], {"error": str(exc), "status": exc.code}
      except Exception as exc:  # source failure is data, not a pipeline crash
        log.source_log("open-source", f"request failed: {exc}", tty_only=False)
        return [], {"error": str(exc), "status": getattr(exc, "code", None) or 0}

def _date(value: Any) -> str:
    if not value:
        return ""
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).date().isoformat()
    except ValueError:
        return text[:10]

def _item(source: str, title: str, url: str, snippet: str = "", published: Any = "", author: str = "") -> dict[str, Any]:
    return {"source": source, "title": title, "url": url, "snippet": snippet, "date": _date(published), "author": author}

def search_arxiv_atom(query: str, from_date: str, to_date: str, depth: str = "default") -> dict[str, Any]:
    q = urllib.parse.quote(f"all:{query}")
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    url = f"https://export.arxiv.org/api/query?search_query={q}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    root, meta = _get(url)
    if not isinstance(root, ET.Element):
        return {"results": [], **meta}
    ns = {"a": "http://www.w3.org/2005/Atom"}
    rows = []
    for entry in root.findall("a:entry", ns):
        link = next((x.attrib.get("href", "") for x in entry.findall("a:link", ns) if x.attrib.get("rel") == "alternate"), "")
        rows.append(_item("arxiv_atom", entry.findtext("a:title", "", ns).strip().replace("\n", " "), link, entry.findtext("a:summary", "", ns).strip(), entry.findtext("a:published", "", ns), entry.findtext("a:author/a:name", "", ns)))
    return {"results": rows, **meta}

def search_semantic_scholar(query: str, from_date: str, to_date: str, depth: str = "default", api_key: str | None = None) -> dict[str, Any]:
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    params = urllib.parse.urlencode({"query": query, "limit": limit, "fields": "title,abstract,url,publicationDate,authors,year"})
    global _SEMANTIC_LAST
    with _SEMANTIC_LOCK:
        wait = 1.0 - (time.monotonic() - _SEMANTIC_LAST)
        if wait > 0:
            time.sleep(wait)
        headers = {}
        key = api_key or os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        if key:
            headers["x-api-key"] = key
        data, meta = _get(f"https://api.semanticscholar.org/graph/v1/paper/search?{params}", headers)
        _SEMANTIC_LAST = time.monotonic()
    rows = []
    for paper in data.get("data", []) if isinstance(data, dict) else []:
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", [])[:3])
        rows.append(_item("semantic_scholar", paper.get("title", ""), paper.get("url", ""), paper.get("abstract", "") or "", paper.get("publicationDate") or paper.get("year"), authors))
    return {"results": rows, **meta}

def search_crossref(query: str, from_date: str, to_date: str, depth: str = "default") -> dict[str, Any]:
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    params = urllib.parse.urlencode({"query": query, "rows": limit, "filter": f"from-pub-date:{from_date},until-pub-date:{to_date}"})
    data, meta = _get(f"https://api.crossref.org/works?{params}", {"mailto": "last30days@example.invalid"})
    rows = []
    for work in data.get("message", {}).get("items", []) if isinstance(data, dict) else []:
        title = (work.get("title") or [""])[0]
        authors = ", ".join(a.get("family", "") for a in work.get("author", [])[:3])
        rows.append(_item("crossref", title, work.get("URL", ""), work.get("abstract", ""), (work.get("published-print") or work.get("published-online") or {}).get("date-parts", [[""]])[0][0], authors))
    return {"results": rows, **meta}

def search_huggingface(query: str, from_date: str, to_date: str, depth: str = "default") -> dict[str, Any]:
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    # Fetch a wider, recency-sorted pool, then apply a local date filter. The
    # Hub search endpoint does not consistently honor date constraints across
    # task types, so local filtering is more predictable.
    voice_terms = "voice audio speech text-to-speech automatic-speech-recognition"
    task_filter = voice_terms if any(t in query.lower() for t in ("voice", "speech", "audio", "tts", "stt")) else ""
    params = urllib.parse.urlencode({"search": query, "limit": max(limit, 50), "sort": "lastModified", "direction": "-1", "full": "true"})
    data, meta = _get(f"https://huggingface.co/api/models?{params}")
    rows = []
    for model in data if isinstance(data, list) else []:
        ident = model.get("id", "")
        haystack = " ".join(str(x) for x in [ident, model.get("pipeline_tag", ""), *model.get("tags", [])]).lower()
        if task_filter and not any(term in haystack for term in task_filter.split()):
            continue
        modified = _date(model.get("lastModified"))
        if modified and not (from_date <= modified <= to_date):
            continue
        tags = ", ".join(model.get("pipeline_tag") and [model.get("pipeline_tag")] or model.get("tags", [])[:5])
        rows.append(_item("huggingface", ident, f"https://huggingface.co/{ident}", f"task={tags}; downloads={model.get('downloads', 0)} likes={model.get('likes', 0)}", model.get("lastModified"), model.get("author", "")))
        if len(rows) >= limit:
            break
    return {"results": rows, **meta}

def search_github_api(query: str, from_date: str, to_date: str, depth: str = "default", token: str | None = None) -> dict[str, Any]:
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    params = urllib.parse.urlencode({"q": f"{query} created:{from_date}..{to_date}", "per_page": limit, "sort": "stars", "order": "desc"})
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data, meta = _get(f"https://api.github.com/search/repositories?{params}", headers)
    rows = []
    for repo in data.get("items", []) if isinstance(data, dict) else []:
        rows.append(_item("github_api", repo.get("full_name", ""), repo.get("html_url", ""), repo.get("description", "") or "", repo.get("created_at"), repo.get("owner", {}).get("login", "")))
    return {"results": rows, **meta}

def search_openreview(query: str, from_date: str, to_date: str, depth: str = "default") -> dict[str, Any]:
    limit = {"quick": 5, "default": 10, "deep": 20}.get(depth, 10)
    params = urllib.parse.urlencode({"content.title": query, "limit": limit})
    data, meta = _get(f"https://api2.openreview.net/notes?{params}")
    if not isinstance(data, dict) or not data.get("notes"):
        # OpenReview has operated both api2 and api endpoints. Try the public
        # legacy endpoint before declaring the source unavailable.
        data, meta = _get(f"https://api.openreview.net/notes?{params}")
    rows = []
    for note in data.get("notes", []) if isinstance(data, dict) else []:
        content = note.get("content", {})
        title = content.get("title", {}).get("value", "") if isinstance(content.get("title"), dict) else str(content.get("title", ""))
        rows.append(_item("openreview", title, f"https://openreview.net/forum?id={note.get('id', '')}", str(content.get("abstract", "")), note.get("cdate") or note.get("mdate"), ""))
    return {"results": rows, **meta}

def parse(result: dict[str, Any], source: str) -> list[dict[str, Any]]:
    return [dict(item, source=source) for item in result.get("results", []) if isinstance(item, dict)]
