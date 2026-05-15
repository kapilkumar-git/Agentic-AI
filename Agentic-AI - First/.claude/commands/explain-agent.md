Read the file agent.py in the current project directory.

Then explain the following in plain English, referencing the actual code (file path and line numbers):

1. **Agentic Loop** — walk through the `while True:` loop step by step. Explain what happens on each iteration, what `stop_reason` values mean, and how tool results are fed back into the conversation.

2. **Tools** — explain what tools are, how Claude decides to use them, and walk through each of the three tools defined in this file: what it does, its input schema, and where it's implemented.

3. **Prompt Caching** — explain what `cache_control: ephemeral` does on the system prompt and why it saves cost and latency.

Keep the explanation clear enough for someone new to the Anthropic API but familiar with Python.
