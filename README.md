# 🔍 Web Research Agent

An AI-powered research agent that answers any question by autonomously searching the web, reading sources, and synthesizing a clear, cited report — all from your terminal.

Built with Python + [Anthropic Claude](https://www.anthropic.com/) using the **tool use (function calling)** pattern at the core of modern AI agents.

---

## ✨ Demo

```
❓ Your question: What are the latest breakthroughs in nuclear fusion energy?

[10:32:01] 🔍 Research Agent started
           Question: What are the latest breakthroughs in nuclear fusion energy?
[10:32:03] 🛠  Using tool: search_web
           {'query': 'nuclear fusion energy breakthroughs 2024', 'num_results': 5}
[10:32:04] 📥 Tool result: search_web
           Got 1847 chars
[10:32:04] 🛠  Using tool: scrape_url
           {'url': 'https://www.science.org/...'}
[10:32:06] 📥 Tool result: scrape_url
           Got 4203 chars
[10:32:09] ✅ Research complete
           Used 3 sources over 4 iterations

──────────────────────────────────────────────────────────────────────
  🔬  WEB RESEARCH AGENT — REPORT
──────────────────────────────────────────────────────────────────────
  Question : What are the latest breakthroughs in nuclear fusion energy?
  Generated: 2024-11-15 10:32:09
──────────────────────────────────────────────────────────────────────

  ## Nuclear Fusion: Recent Breakthroughs

  In December 2022, the National Ignition Facility (NIF) at Lawrence Livermore
  achieved a historic milestone: ignition — producing more energy from fusion
  than the laser energy used to trigger it...
  
  [Full cited report follows]
```

---

## 🏗️ How It Works

```
User Question
     │
     ▼
┌─────────────────────────────────────────┐
│           Research Agent Loop           │
│                                         │
│  Claude (claude-opus-4-5)               │
│       │                                 │
│       ├──► search_web(query)            │
│       │         └──► DuckDuckGo API     │
│       │                                 │
│       ├──► scrape_url(url)              │
│       │         └──► requests + BS4     │
│       │                                 │
│       └──► [enough info?] ──► Answer   │
└─────────────────────────────────────────┘
     │
     ▼
Formatted Report (terminal + optional .txt)
```

The agent uses a **ReAct-style loop** (Reason → Act → Observe → Repeat):
1. Claude decides what to search for
2. It reads the results and picks URLs to scrape
3. It synthesizes information across sources
4. When confident, it writes a cited final answer

---

## 📁 Project Structure

```
web-research-agent/
├── main.py               # CLI entry point
├── requirements.txt      # Dependencies
├── .env.example          # Environment variable template
│
├── agent/
│   ├── __init__.py
│   └── researcher.py     # Core agent loop (tool use orchestration)
│
├── tools/
│   ├── __init__.py
│   ├── search.py         # DuckDuckGo web search
│   └── scraper.py        # URL fetcher + text extractor
│
├── utils/
│   ├── __init__.py
│   ├── logger.py         # Colored terminal output
│   └── formatter.py      # Report formatting + file saving
│
└── tests/
    └── test_tools.py     # Unit tests
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/web-research-agent.git
cd web-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here
```

Get a free API key at [console.anthropic.com](https://console.anthropic.com/).

---

## 💻 Usage

### Interactive mode (recommended for beginners)

```bash
python main.py
```

### Single question mode

```bash
python main.py "What is the James Webb Space Telescope discovering?"
```

### Save report to file

```bash
python main.py "Explain the difference between RAG and fine-tuning" --save
```

### Quiet mode (only show final answer)

```bash
python main.py "Who invented the transformer architecture?" --quiet
```

### All options

```
usage: main.py [-h] [--save] [--quiet] [--max-iter MAX_ITER] [question]

positional arguments:
  question             Research question (omit for interactive mode)

options:
  -h, --help           show this help message and exit
  --save, -s           Save the report to a .txt file
  --quiet, -q          Suppress step-by-step logs
  --max-iter MAX_ITER  Maximum agent iterations (default: 10)
```

---

## 🧪 Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## 🔧 Key Concepts Demonstrated

| Concept | Where |
|---|---|
| LLM Tool Use / Function Calling | `agent/researcher.py` |
| Agentic ReAct Loop | `agent/researcher.py` |
| Web Scraping | `tools/scraper.py` |
| Search API Integration | `tools/search.py` |
| Prompt Engineering | `agent/researcher.py` → `SYSTEM_PROMPT` |
| Multi-turn Conversation History | `agent/researcher.py` → `messages` list |
| CLI with argparse | `main.py` |

---

## 🛠️ Extending the Agent

Some ideas to make this your own:

- **Add more tools**: Calculator, Wikipedia API, YouTube transcript reader
- **Add memory**: Save past research to a JSON file and reference it
- **Web UI**: Wrap with Streamlit for a browser-based interface
- **Export to PDF**: Use `reportlab` to save formatted PDF reports
- **Scheduled research**: Use `schedule` lib to run daily research digests

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `anthropic` | Claude API client (LLM + tool use) |
| `duckduckgo-search` | Free web search (no API key needed) |
| `requests` | HTTP client for URL fetching |
| `beautifulsoup4` | HTML parsing and text extraction |

---

---

## 🙋 Author

Built as a learning project to explore AI agent patterns.  
Feel free to fork, star ⭐, and build on top of it!
