"""
Formats the final research report for display and file saving.
"""

import datetime
from typing import List


DIVIDER = "─" * 70


def format_report(question: str, answer: str, sources: List[str]) -> str:
    """
    Wrap the agent's answer in a nicely formatted report.

    Args:
        question: The original research question
        answer:   The agent's final answer text
        sources:  List of URLs used during research

    Returns:
        A formatted string report
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "",
        DIVIDER,
        "  🔬  WEB RESEARCH AGENT — REPORT",
        DIVIDER,
        f"  Question : {question}",
        f"  Generated: {timestamp}",
        DIVIDER,
        "",
        answer,
        "",
    ]

    if sources:
        lines += [
            DIVIDER,
            "  📚  Sources consulted:",
        ]
        for i, src in enumerate(sources, 1):
            lines.append(f"  [{i}] {src}")

    lines += [DIVIDER, ""]

    return "\n".join(lines)


def save_report(report: str, filename: str = "") -> str:
    """
    Save the report to a text file.

    Args:
        report:   The formatted report string
        filename: Optional filename (auto-generated if empty)

    Returns:
        The path where the report was saved
    """
    if not filename:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{ts}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    return filename
