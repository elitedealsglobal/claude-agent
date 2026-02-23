# claude-agent

A research agent powered by the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python). Ask a question, and it searches the web, reads pages, cross-references facts, and returns a structured answer with sources.

## Features

- **Web research** — searches the web and reads full pages for detail
- **Deep mode** — broader searches, more sources, higher turn limit
- **Fact-checker subagent** — verifies claims via independent sources (runs on Haiku for cost efficiency)
- **Adaptive thinking** — Claude reasons more deeply when the question demands it
- **Live tool activity** — see what the agent is searching and reading in real time
- **Session resumption** — ask follow-up questions without losing context
- **File output** — save results to markdown with timestamps

## Prerequisites

- **Python 3.10+**
- **Node.js** (for the Claude Code CLI)
- **Anthropic API key** — get one at [console.anthropic.com](https://console.anthropic.com/)

## Setup

```bash
# 1. Install the Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 2. Clone and enter the project
git clone https://github.com/elitedealsglobal/claude-agent.git
cd claude-agent

# 3. Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set your API key (pick one method)
#    Option A: environment variable
set ANTHROPIC_API_KEY=your_key_here          # Windows
# export ANTHROPIC_API_KEY=your_key_here     # macOS/Linux

#    Option B: .env file
copy .env.example .env
#    then edit .env and fill in your key
```

## Usage

```bash
# Ask a question
python main.py "What are the latest advances in quantum computing?"

# Interactive mode (prompts for input)
python main.py

# Deep research (more searches, more sources)
python main.py --deep "How does mRNA vaccine technology work?"

# Save output to a file
python main.py -o report.md "History of the internet"

# Quiet mode (no tool activity, just the answer)
python main.py -q "What is dark matter?"

# Resume a previous session for follow-up questions
python main.py --resume SESSION_ID "Tell me more about the third point"
```

## CLI Reference

```
usage: main.py [-h] [-o OUTPUT] [--deep] [--resume SESSION_ID]
               [--max-turns MAX_TURNS] [-q]
               [question]

positional arguments:
  question              Research question (omit for interactive mode)

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Save the final answer to a file
  --deep                Use deeper research mode (more searches, more sources)
  --resume SESSION_ID   Resume a previous session for follow-up questions
  --max-turns MAX_TURNS Max agent turns (default: 15, deep mode: 30)
  -q, --quiet           Suppress tool activity output, show only the answer
```

## How It Works

```
You ask a question
       |
       v
  Agent searches the web (multiple queries)
       |
       v
  Reads the most relevant pages
       |
       v
  Cross-references facts across sources
       |
       v
  (Optional) Fact-checker subagent verifies claims
       |
       v
  Returns a structured answer with sources
```

## Project Structure

```
claude-agent/
  main.py             # The research agent
  requirements.txt    # Python dependencies
  .env.example        # API key template
  .gitignore          # Keeps secrets and junk out of git
  LICENSE             # MIT license
  README.md           # Setup and CLI reference
  HOW-TO-USE.md       # Beginner-friendly guide
```

## License

MIT
