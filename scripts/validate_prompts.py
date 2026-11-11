#!/usr/bin/env python3
"""Validate the prompt catalog."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_prompt_library import PromptLibrary


def main() -> int:
    errors = PromptLibrary.load().validate()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Prompt library is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
