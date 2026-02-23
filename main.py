"""
Research Agent — powered by the Claude Agent SDK.

A research agent that searches the web, reads pages, and synthesizes
findings. Features: live tool activity display, adaptive thinking,
subagents for fact-checking, session resumption for follow-ups, and
optional file output.

Prerequisites:
    1. Install the Claude Code CLI:  npm install -g @anthropic-ai/claude-code
    2. Install Python deps:          pip install -r requirements.txt
    3. Set your API key:             set ANTHROPIC_API_KEY=your_key  (Windows)
       — or copy .env.example to .env and fill in the key there

Usage:
    python main.py "What are the latest advances in quantum computing?"
    python main.py                                  # interactive mode
    python main.py -o report.md "your question"     # save to file
    python main.py --deep "your question"           # more thorough research
    python main.py --resume SESSION_ID "follow-up"  # continue a session
"""

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from claude_agent_sdk import (
    query,
    AgentDefinition,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
)

load_dotenv()

SYSTEM_PROMPT = """\
You are a thorough research assistant. For every question:
1. Search the web for multiple authoritative, up-to-date sources.
2. Open and read the most relevant pages for deeper detail.
3. Cross-reference facts across sources to ensure accuracy.
4. Synthesize findings into a clear, well-structured answer.
5. End with a "Sources" section listing each URL you used.
Be concise but comprehensive. Prefer recent sources. Flag any \
conflicting information you find."""

DEEP_SYSTEM_PROMPT = """\
You are an expert research analyst performing deep research. For every question:
1. Search the web broadly — use multiple distinct search queries to cover \
different angles of the topic.
2. Open and read at least 3-5 of the most authoritative pages in full.
3. Cross-reference facts across sources. Note and flag any conflicts.
4. Organize your answer with clear headings and bullet points.
5. Include a "Key Findings" summary at the top.
6. End with a "Sources" section listing every URL consulted.
Be thorough. Pursue follow-up searches when initial results are insufficient. \
Prioritize primary sources and recent publications."""

# Subagent: a fact-checker that verifies claims
FACT_CHECKER_AGENT = AgentDefinition(
    description="Verifies factual claims by cross-referencing multiple sources.",
    prompt=(
        "You are a fact-checker. When given a claim, search for independent "
        "sources that confirm or deny it. Report whether the claim is "
        "supported, disputed, or unverifiable, with source URLs."
    ),
    tools=["WebSearch", "WebFetch"],
    model="haiku",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Research agent powered by Claude Agent SDK",
    )
    p.add_argument(
        "question",
        nargs="?",
        help="Research question (omit for interactive mode)",
    )
    p.add_argument(
        "-o", "--output",
        help="Save the final answer to a file",
    )
    p.add_argument(
        "--deep",
        action="store_true",
        help="Use deeper research mode (more searches, more sources)",
    )
    p.add_argument(
        "--resume",
        metavar="SESSION_ID",
        help="Resume a previous session for follow-up questions",
    )
    p.add_argument(
        "--max-turns",
        type=int,
        default=15,
        help="Max agent turns (default: 15, deep mode: 30)",
    )
    p.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress tool activity output, show only the answer",
    )
    return p.parse_args()


def print_tool_activity(block: ToolUseBlock) -> None:
    """Print a short line showing what tool the agent is using."""
    name = block.name
    inp = block.input
    if name == "WebSearch":
        print(f"  >> Searching: {inp.get('query', '')}", flush=True)
    elif name == "WebFetch":
        url = inp.get("url", "")
        print(f"  >> Reading:   {url[:80]}", flush=True)
    elif name == "Grep":
        print(f"  >> Grep: {inp.get('pattern', '')}", flush=True)
    elif name == "Glob":
        print(f"  >> Glob: {inp.get('pattern', '')}", flush=True)
    elif name == "Read":
        print(f"  >> Read: {inp.get('file_path', '')}", flush=True)
    elif name == "Task":
        print(f"  >> Subagent: {inp.get('description', name)}", flush=True)
    else:
        print(f"  >> {name}", flush=True)


async def run_agent(args: argparse.Namespace) -> None:
    question = args.question
    if not question:
        question = input("Enter your research question: ").strip()
        if not question:
            print("No question provided.", file=sys.stderr)
            sys.exit(1)

    print(f"\nResearch question: {question}")
    if args.deep:
        print("[Deep research mode]")
    print()

    system_prompt = DEEP_SYSTEM_PROMPT if args.deep else SYSTEM_PROMPT
    max_turns = args.max_turns if args.max_turns != 15 else (30 if args.deep else 15)

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=["WebSearch", "WebFetch", "Read", "Glob", "Grep", "Task"],
        permission_mode="bypassPermissions",
        max_turns=max_turns,
        thinking={"type": "adaptive"},
        agents={
            "fact-checker": FACT_CHECKER_AGENT,
        },
    )

    if args.resume:
        options.resume = args.resume

    session_id = None
    final_text = []

    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, flush=True)
                    final_text.append(block.text)
                elif isinstance(block, ToolUseBlock) and not args.quiet:
                    print_tool_activity(block)

        elif isinstance(message, ResultMessage):
            session_id = message.session_id

            if message.is_error:
                print("\n[Warning: agent ended with an error]", flush=True)

            duration = message.duration_ms / 1000
            print(f"\n[Completed in {duration:.1f}s", end="")
            if message.total_cost_usd is not None:
                print(f" | Cost: ${message.total_cost_usd:.4f}", end="")
            print(f" | Turns: {message.num_turns}]")

            if session_id:
                print(f"[Session: {session_id}]")
                print("  (use --resume to continue this conversation)")

    # Save to file if requested
    if args.output and final_text:
        output_path = Path(args.output)
        header = (
            f"# Research: {question}\n"
            f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n\n"
        )
        output_path.write_text(header + "\n".join(final_text), encoding="utf-8")
        print(f"\nSaved to {output_path}")


async def main() -> None:
    args = parse_args()
    try:
        await run_agent(args)
    except CLINotFoundError:
        print(
            "Error: Claude Code CLI not found.\n"
            "Install it with: npm install -g @anthropic-ai/claude-code",
            file=sys.stderr,
        )
        sys.exit(1)
    except ProcessError as e:
        print(f"Error: Agent process failed: {e}", file=sys.stderr)
        sys.exit(1)
    except CLIJSONDecodeError as e:
        print(f"Error: Could not parse SDK response: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
