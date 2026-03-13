"""Claude API client with agentic loop, streaming, and adaptive thinking."""

import anthropic
from tools import get_tool_definitions, execute_tool
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS, MAX_TOOL_ITERATIONS, SYSTEM_PROMPT


def create_client() -> anthropic.Anthropic:
    """Create an Anthropic client instance."""
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def run_agent(
    user_message: str,
    *,
    client: anthropic.Anthropic | None = None,
    messages: list | None = None,
    system: str = SYSTEM_PROMPT,
    stream: bool = True,
) -> str:
    """Run a single agentic turn: send a message, handle tool calls in a loop.

    Args:
        user_message: The user's input message.
        client: Optional pre-created Anthropic client.
        messages: Optional existing conversation history (for multi-turn).
        system: System prompt override.
        stream: Whether to stream the response (recommended for long outputs).

    Returns:
        The final text response from Claude.
    """
    if client is None:
        client = create_client()

    if messages is None:
        messages = []

    messages.append({"role": "user", "content": user_message})
    tools = get_tool_definitions()

    for iteration in range(MAX_TOOL_ITERATIONS):
        if stream:
            response = _stream_response(client, messages, tools, system)
        else:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                thinking={"type": "adaptive"},
                messages=messages,
                tools=tools if tools else anthropic.NOT_GIVEN,
            )

        # Append assistant response to conversation history
        messages.append({"role": "assistant", "content": response.content})

        # If Claude is done (no more tool calls), return the final text
        if response.stop_reason == "end_turn":
            return _extract_text(response)

        # If server-side tool hit iteration limit, re-send to continue
        if response.stop_reason == "pause_turn":
            continue

        # Handle tool use
        if response.stop_reason == "tool_use":
            tool_results = _process_tool_calls(response)
            messages.append({"role": "user", "content": tool_results})
            continue

        # Unexpected stop reason
        break

    return _extract_text(response)


def _stream_response(client, messages, tools, system):
    """Stream a response, printing text deltas in real time."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        thinking={"type": "adaptive"},
        messages=messages,
        tools=tools if tools else anthropic.NOT_GIVEN,
    ) as stream:
        for event in stream:
            if event.type == "content_block_start":
                if event.content_block.type == "thinking":
                    print("\n[thinking...]", flush=True)
                elif event.content_block.type == "text":
                    pass  # text deltas handled below

            elif event.type == "content_block_delta":
                if event.delta.type == "thinking_delta":
                    pass  # suppress thinking output by default
                elif event.delta.type == "text_delta":
                    print(event.delta.text, end="", flush=True)

        return stream.get_final_message()


def _process_tool_calls(response) -> list[dict]:
    """Extract tool_use blocks, execute tools, and return tool_result blocks."""
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"\n> Tool: {block.name}({block.input})", flush=True)
            result = execute_tool(block.name, block.input)
            print(f"  Result: {result[:200]}{'...' if len(result) > 200 else ''}", flush=True)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
    return tool_results


def _extract_text(response) -> str:
    """Extract all text blocks from a response."""
    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)
    return "\n".join(parts)


def run_conversation(*, system: str = SYSTEM_PROMPT, stream: bool = True):
    """Run an interactive multi-turn conversation loop.

    Type 'quit' or 'exit' to end the session.
    """
    client = create_client()
    messages = []
    print("Hermes Agent (Claude API) — type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        if not user_input:
            continue

        print("\nHermes: ", end="", flush=True)
        run_agent(
            user_input,
            client=client,
            messages=messages,
            system=system,
            stream=stream,
        )
        print("\n")
