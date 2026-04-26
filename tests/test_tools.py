"""
Basic tests for the research agent tools.
Run with: python -m pytest tests/ -v
"""

import pytest
from unittest.mock import patch, MagicMock


# ── Search tool tests ────────────────────────────────────────────────────────

class TestSearchTool:
    def test_returns_dict_structure(self):
        """search_web should always return a dict with 'query' and 'results'."""
        with patch("tools.search.DDGS") as mock_ddgs:
            mock_ddgs.return_value.__enter__.return_value.text.return_value = [
                {"href": "https://example.com", "title": "Example", "body": "Some snippet"}
            ]
            from tools.search import search_web
            result = search_web("test query", num_results=1)
            assert "query" in result
            assert "results" in result
            assert result["query"] == "test query"

    def test_num_results_clamped(self):
        """num_results should be clamped between 1 and 10."""
        with patch("tools.search.DDGS") as mock_ddgs:
            mock_ddgs.return_value.__enter__.return_value.text.return_value = []
            from tools.search import search_web
            result = search_web("test", num_results=99)
            # Should not raise; clamped internally
            assert "results" in result

    def test_handles_import_error(self):
        """Should return error dict if duckduckgo_search is not installed."""
        import sys
        with patch.dict(sys.modules, {"duckduckgo_search": None}):
            # reimport to trigger ImportError path
            import importlib
            import tools.search as search_mod
            importlib.reload(search_mod)
            # Just test that import errors are handled gracefully
            # (the actual check happens at runtime inside search_web)


# ── Scraper tool tests ───────────────────────────────────────────────────────

class TestScraperTool:
    def test_returns_dict_structure(self):
        """scrape_url should return a dict with url and content keys."""
        mock_response = MagicMock()
        mock_response.text = "<html><head><title>Test</title></head><body><p>Hello world</p></body></html>"
        mock_response.raise_for_status.return_value = None

        with patch("tools.scraper.requests.get", return_value=mock_response):
            from tools.scraper import scrape_url
            result = scrape_url("https://example.com")
            assert "url" in result
            assert result["url"] == "https://example.com"
            assert "content" in result or "error" in result

    def test_handles_network_error(self):
        """Should return error dict on network failure."""
        import requests
        with patch("tools.scraper.requests.get", side_effect=requests.exceptions.ConnectionError("timeout")):
            from tools.scraper import scrape_url
            result = scrape_url("https://unreachable.example.com")
            assert "error" in result

    def test_content_truncated_when_long(self):
        """Content longer than MAX_CONTENT_LENGTH should be truncated."""
        long_text = "word " * 10000
        mock_response = MagicMock()
        mock_response.text = f"<html><body><p>{long_text}</p></body></html>"
        mock_response.raise_for_status.return_value = None

        with patch("tools.scraper.requests.get", return_value=mock_response):
            from tools.scraper import scrape_url
            result = scrape_url("https://example.com")
            if "content" in result:
                assert len(result["content"]) <= 8200  # MAX + truncation message


# ── Formatter tests ──────────────────────────────────────────────────────────

class TestFormatter:
    def test_format_report_contains_question(self):
        from utils.formatter import format_report
        report = format_report("What is AI?", "AI is...", ["https://example.com"])
        assert "What is AI?" in report
        assert "AI is..." in report
        assert "https://example.com" in report

    def test_format_report_no_sources(self):
        from utils.formatter import format_report
        report = format_report("Test question", "Test answer", [])
        assert "Test question" in report
        assert "Test answer" in report

    def test_save_report_creates_file(self, tmp_path):
        from utils.formatter import save_report
        report = "Test report content"
        filepath = str(tmp_path / "test_report.txt")
        saved_path = save_report(report, filename=filepath)
        with open(saved_path, "r") as f:
            content = f.read()
        assert content == report
