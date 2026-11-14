"""Public GitHub Trending repository listings with measured weekly stars."""

from __future__ import annotations

import html
import re
import urllib.request
from datetime import date


URL = "https://github.com/trending?since=weekly"
_CARD = re.compile(r'<article\b[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>', re.S)
_REPO = re.compile(r'<h2\b[^>]*>.*?<a\b[^>]*href="/([\w.-]+/[\w.-]+)"', re.S)
_WEEKLY = re.compile(r'([\d,]+)\s+stars this week', re.I)
_DESC = re.compile(r'<p\b[^>]*>(.*?)</p>', re.S)


def parse_weekly(html_text: str, *, as_of: str | None = None) -> list[dict]:
    """Return only cards that expose GitHub's own weekly star metric."""
    stamp = as_of or date.today().isoformat()
    items = []
    for card in _CARD.findall(html_text):
        repo = _REPO.search(card)
        weekly = _WEEKLY.search(card)
        if not repo or not weekly:
            continue
        name = html.unescape(repo.group(1))
        stars = int(weekly.group(1).replace(",", ""))
        description = _DESC.search(card)
        summary = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", description.group(1) if description else ""))).strip()
        items.append({
            "id": f"trending-{name.lower()}",
            "title": f"GitHub repository {name}",
            "snippet": summary,
            "url": f"https://github.com/{name}",
            "author": name.split("/", 1)[0],
            "container": "GitHub Trending",
            "date": stamp,
            "engagement": {"stars_this_week": stars},
            "relevance": 0.95,
            "why_relevant": f"GitHub Trending: {stars:,} stars this week",
            "metadata": {"date_is_snapshot": True},
        })
    return sorted(items, key=lambda item: item["engagement"]["stars_this_week"], reverse=True)


def fetch_weekly(*, as_of: str | None = None) -> list[dict]:
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (last30days research)", "Accept": "text/html"})
    with urllib.request.urlopen(request, timeout=15) as response:
        content = response.read(2_000_000).decode("utf-8", "replace")
    items = parse_weekly(content, as_of=as_of)
    if not items:
        raise ValueError("GitHub Trending returned no repository cards with weekly star counts")
    return items
