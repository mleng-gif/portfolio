import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-opus-4-6"
MAX_TOKENS = 16000
MAX_TOOL_ITERATIONS = 25
SYSTEM_PROMPT = """You are Hermes, an autonomous AI agent. You solve complex tasks step by step,
using tools when needed. Think carefully before acting. Break problems into smaller steps
and verify your work as you go."""
