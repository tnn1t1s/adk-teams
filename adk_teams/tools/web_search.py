import os
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SERPER_API_KEY = os.environ["SERPER_API_KEY"]
SERPER_URL = "https://google.serper.dev/search"


def web_search(query: str, num_results: int = 5) -> dict:
    """Searches the web using Serper for evidence to support critique findings.

    Args:
        query: Short, specific search query (5-10 words).
        num_results: Number of results to return (default 5, max 10).

    Returns:
        dict: status and list of search results with title, link, and snippet.
    """
    num_results = min(max(num_results, 1), 10)

    payload = json.dumps({"q": query, "num": num_results}).encode()

    req = Request(
        SERPER_URL,
        data=payload,
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except (HTTPError, URLError) as e:
        return {"status": "error", "query": query, "error": str(e)}

    results = []
    for item in data.get("organic", [])[:num_results]:
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    return {"status": "success", "query": query, "results": results}
