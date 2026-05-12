import sys
from datetime import datetime
import anthropic

client = anthropic.Anthropic()

# --- Tool definitions ---

tools = [
    {
        "name": "calculate",
        "description": (
            "Evaluate a safe mathematical expression and return the numeric result. "
            "Use this whenever the user needs arithmetic, powers, or math calculations. "
            "Examples: '2 ** 32', '(100 * 1.08) / 12', 'round(3.14159 * 5**2, 2)'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python math expression using numbers and operators: + - * / ** // % round()"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Return the current local date and time. Use this when the user asks what time or date it is.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "search_web",
        "description": (
            "Simulate a web search and return a short summary. "
            "Use this when the user asks about current events, facts, or anything you are unsure about."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string"
                }
            },
            "required": ["query"]
        }
    }
]

# --- Tool implementations ---

SAFE_MATH = {name: getattr(__builtins__ if isinstance(__builtins__, dict) else __builtins__, name, None)
             for name in ["abs", "round", "min", "max", "sum", "pow"]}

def run_tool(name: str, inputs: dict) -> str:
    if name == "calculate":
        try:
            result = eval(inputs["expression"], {"__builtins__": {}}, SAFE_MATH)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    if name == "get_current_time":
        return datetime.now().strftime("%A, %B %d %Y — %I:%M %p")

    if name == "search_web":
        # Stub: replace with a real search API (e.g. Brave, Serper) if desired
        return f"[stub] Search results for '{inputs['query']}': No live search configured. Answer from your own knowledge."

    return f"Unknown tool: {name}"

# --- Agentic loop ---

def run_agent(user_query: str):
    print(f"\nUser: {user_query}\n")

    # System prompt with cache_control so it's reused across turns (saves cost)
    system = [
        {
            "type": "text",
            "text": (
                "You are a helpful assistant. "
                "Use tools whenever they help you give a more accurate or up-to-date answer. "
                "You may call multiple tools in a single turn if needed."
            ),
            "cache_control": {"type": "ephemeral"}
        }
    ]

    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages,
        )

        # Append Claude's reply to history
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            print("Claude:", end=" ")
            for block in response.content:
                if hasattr(block, "text"):
                    print(block.text)
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [tool call]  {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    print(f"  [tool result] {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            # Feed all results back in one user turn
            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason — print whatever we have and exit
            print(f"Stopped: {response.stop_reason}")
            break

# --- Entry point ---

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "What is 2**32, and what day of the week is it today?"
    run_agent(query)
