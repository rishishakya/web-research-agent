"""
URL scraper tool - fetches and extracts clean text from web pages.
"""

import re
from typing import Optional


MAX_CONTENT_LENGTH = 8000  # characters to return (keeps token usage reasonable)


def scrape_url(url: str, timeout: int = 10) -> dict:
    """
    Fetch a URL and extract its main text content.

    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds

    Returns:
        Dict with 'url', 'title', 'content', and optional 'error'
    """
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise elements
        for tag in soup(["script", "style", "nav", "footer", "header",
                          "aside", "form", "iframe", "noscript", "ads"]):
            tag.decompose()

        # Get title
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)

        # Try to find main content area
        main = (
            soup.find("main") or
            soup.find("article") or
            soup.find(id=re.compile(r"content|main|article", re.I)) or
            soup.find(class_=re.compile(r"content|main|article|post", re.I)) or
            soup.body
        )

        if main:
            text = main.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        # Truncate if too long
        if len(clean_text) > MAX_CONTENT_LENGTH:
            clean_text = clean_text[:MAX_CONTENT_LENGTH] + "\n\n[Content truncated...]"

        return {
            "url": url,
            "title": title,
            "content": clean_text,
            "length": len(clean_text)
        }

    except ImportError as e:
        return {
            "url": url,
            "error": f"Missing dependency: {e}. Run: pip install requests beautifulsoup4"
        }
    except Exception as e:
        return {
            "url": url,
            "error": f"Failed to scrape {url}: {str(e)}"
        }
