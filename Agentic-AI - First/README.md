# Agentic-AI — agent.py

A minimal agentic AI assistant built with the Anthropic Python SDK and `claude-sonnet-4-6`.

## What it does

The agent takes a user query, sends it to Claude, and loops until Claude produces a final answer. Along the way, Claude can call local tools to fetch data or perform calculations before responding.

## Agentic Loop

The core of the agent is a `while True:` loop in `run_agent()`:

1. Send the conversation history (user message + any prior tool results) to Claude.
2. Claude responds with either:
   - `end_turn` — a final answer. Print it and stop.
   - `tool_use` — one or more tool calls. Run them locally, collect results, send back.
3. Repeat until `end_turn`.

This loop is what makes the assistant "agentic": it can take multiple reasoning steps, observe tool output, and decide what to do next before giving a final answer.

## Tools

Tools are functions you expose to Claude so it can act, not just answer. Each tool has three parts:

| Part | Purpose |
|---|---|
| `name` | How Claude refers to the tool |
| `description` | Tells Claude *when* to use it |
| `input_schema` | JSON Schema defining the arguments |

Claude does not call tools directly — it returns a `tool_use` block with the tool name and arguments. The Python code runs the function and sends the result back in the next message.

### Available tools

| Tool | What it does |
|---|---|
| `calculate` | Evaluates a math expression safely using Python `eval` |
| `get_current_time` | Returns the current local date and time |
| `search_web` | Stub for web search (replace with Brave/Serper API for live results) |

## Prompt Caching

The system prompt uses `cache_control: ephemeral` so Anthropic reuses the cached prompt across turns, reducing latency and cost.

## Usage

```bash
# Default query
python3 agent.py

# Custom query
python3 agent.py "What is 15% of 348 and what time is it?"
```

## Requirements

```bash
pip3 install anthropic
```

Set your API key before running:

```bash
export ANTHROPIC_API_KEY=your_key_here
```
