#!/usr/bin/env python3
"""Hermes Agent — main entry point.

Usage:
    # Interactive chat
    python agent.py

    # Single prompt
    python agent.py "Explain how TCP works"

    # Non-streaming (wait for full response)
    python agent.py --no-stream "List files in the current directory"
"""

import sys
from client import run_agent, run_conversation


def main():
    stream = "--no-stream" not in sys.argv
    args = [a for a in sys.argv[1:] if a != "--no-stream"]

    if args:
        # Single-shot mode
        prompt = " ".join(args)
        print("Hermes: ", end="", flush=True)
        result = run_agent(prompt, stream=stream)
        if not stream:
            print(result)
        print()
    else:
        # Interactive conversation mode
        run_conversation(stream=stream)


if __name__ == "__main__":
    main()
