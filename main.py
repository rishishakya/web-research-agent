#!/usr/bin/env python3
"""
Web Research Agent — CLI entry point.

Usage:
    python main.py                          # interactive mode
    python main.py "What is quantum computing?"
    python main.py "..." --save             # save report to file
    python main.py "..." --quiet            # suppress step logs
"""

import argparse
import sys
import os


def check_api_key() -> None:
    """Make sure ANTHROPIC_API_KEY is set."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌  Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("    Set it with:  export ANTHROPIC_API_KEY=your_key_here")
        print("    Get a key at: https://console.anthropic.com/")
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="🔍 Web Research Agent — answer questions by searching the web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "What are the latest breakthroughs in fusion energy?"
  python main.py "Best Python frameworks for building REST APIs in 2024" --save
  python main.py --quiet "Who won the 2024 Nobel Prize in Physics?"
        """
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Research question (omit for interactive mode)"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save the report to a .txt file"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress step-by-step logs (only show final answer)"
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=10,
        help="Maximum agent iterations (default: 10)"
    )
    return parser.parse_args()


def run_interactive(args: argparse.Namespace) -> None:
    """Run the agent in an interactive loop."""
    from agent import run_agent
    from utils.formatter import save_report

    print("\n🔍  Web Research Agent  (type 'quit' or 'exit' to stop)\n")

    while True:
        try:
            question = input("❓ Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋  Goodbye!")
            break

        if question.lower() in ("quit", "exit", "q"):
            print("👋  Goodbye!")
            break

        if not question:
            continue

        report = run_agent(
            question,
            max_iterations=args.max_iter,
            verbose=not args.quiet
        )
        print(report)

        if args.save:
            path = save_report(report)
            print(f"💾  Report saved to: {path}\n")


def run_single(question: str, args: argparse.Namespace) -> None:
    """Run the agent for a single question."""
    from agent import run_agent
    from utils.formatter import save_report

    report = run_agent(
        question,
        max_iterations=args.max_iter,
        verbose=not args.quiet
    )
    print(report)

    if args.save:
        path = save_report(report)
        print(f"💾  Report saved to: {path}")


def main() -> None:
    check_api_key()
    args = parse_args()

    if args.question:
        run_single(args.question, args)
    else:
        run_interactive(args)


if __name__ == "__main__":
    main()
