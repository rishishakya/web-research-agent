"""
Web search tool using DuckDuckGo (no API key required).
Falls back to mock results if the library is unavailable.
"""

import time
from typing import Optional


def search_web(query: str, num_results: int = 5) -> dict:
    """
    Search the web using DuckDuckGo and return results.

    Args:
        query: Search query string
        num_results: Number of results to return (1-10)

    Returns:
        Dict with 'results' list containing url, title, snippet
    """
    num_results = min(max(num_results, 1), 10)

    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append({
                    "url": r.get("href", ""),
                    "title": r.get("title", ""),
                    "snippet": r.get("body", "")
                })
                time.sleep(0.1)  # polite delay

        return {
            "query": query,
            "num_results": len(results),
            "results": results
        }

    except ImportError:
        return {
            "error": "duckduckgo_search not installed. Run: pip install duckduckgo-search",
            "query": query,
            "results": []
        }
    except Exception as e:
        return {
            "error": f"Search failed: {str(e)}",
            "query": query,
            "results": []
        }
