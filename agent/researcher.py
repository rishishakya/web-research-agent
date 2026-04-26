"""
Core Research Agent - orchestrates search, scrape, and summarize loop.
"""

import anthropic
from tools.search import search_web
from tools.scraper import scrape_url
from utils.logger import log_step
from utils.formatter import format_report


SYSTEM_PROMPT = """You are a meticulous AI research agent. Your job is to answer user questions by:
1. Searching the web for relevant sources
2. Reading and extracting key information from those sources
3. Synthesizing a clear, accurate, well-structured answer

Always cite your sources. Be concise but thorough. If information conflicts across sources, mention it.
When you have enough information to answer confidently, provide the final answer.
"""

TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for a query and return a list of relevant URLs with titles and snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web."
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 5, max: 10).",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "scrape_url",
        "description": "Fetch and extract the main text content from a given URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to scrape and extract content from."
                }
            },
            "required": ["url"]
        }
    }
]


def run_agent(question: str, max_iterations: int = 10, verbose: bool = True) -> str:
    """
    Run the research agent on a question.

    Args:
        question: The research question to answer
        max_iterations: Maximum number of tool-use loops
        verbose: Whether to print step-by-step progress

    Returns:
        A formatted research report as a string
    """
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    if verbose:
        log_step("🔍 Research Agent started", f"Question: {question}")

    iteration = 0
    sources_used = []

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        # Add assistant response to history
        messages.append({"role": "assistant", "content": response.content})

        # Check if we're done
        if response.stop_reason == "end_turn":
            if verbose:
                log_step("✅ Research complete", f"Used {len(sources_used)} sources over {iteration} iterations")

            # Extract final text
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text = block.text
                    break

            return format_report(question, final_text, sources_used)

        # Process tool calls
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input

                if verbose:
                    log_step(f"🛠  Using tool: {tool_name}", str(tool_input))

                # Execute the tool
                if tool_name == "search_web":
                    result = search_web(
                        query=tool_input["query"],
                        num_results=tool_input.get("num_results", 5)
                    )
                    # Track sources
                    for item in result.get("results", []):
                        if item.get("url") not in sources_used:
                            sources_used.append(item.get("url"))

                elif tool_name == "scrape_url":
                    url = tool_input["url"]
                    result = scrape_url(url)
                    if url not in sources_used:
                        sources_used.append(url)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                if verbose:
                    log_step(f"📥 Tool result: {tool_name}", f"Got {len(str(result))} chars")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

            # Feed tool results back
            messages.append({"role": "user", "content": tool_results})

    return "⚠️ Max iterations reached. The agent could not complete the research in time."
