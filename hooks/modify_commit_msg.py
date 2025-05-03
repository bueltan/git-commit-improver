#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from urllib import request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def call_llama(prompt: str) -> str:
    """Call LLaMA API"""
    data = json.dumps(
        {
            "model": MODEL,
            "prompt": f'Fix spelling and grammar. Only reply with the corrected text:\n\n"{prompt}"',
            "stream": False,
        }
    ).encode("utf-8")

    req = request.Request(OLLAMA_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    with request.urlopen(req) as resp:
        result = json.load(resp)
        return result["response"].strip()


def main():
    """Main entrypoint"""
    if len(sys.argv) < 2:
        sys.exit("Expected path to commit message file as argument.")

    commit_msg_path = Path(sys.argv[1])
    original_msg = commit_msg_path.read_text(encoding="utf-8")

    try:
        improved_msg = call_llama(original_msg)
        commit_msg_path.write_text(improved_msg, encoding="utf-8")
    except Exception as e:
        # Fallback in case of failure — keep original message
        print(f"Warning: failed to get response from LLaMA: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
