"""Command line interface for the prompt library."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .library import PromptLibrary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Browse and render AI prompts.")
    parser.add_argument("--library", default=None, help="Path to a prompt library JSON file.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List prompt ids and titles.")

    search_parser = subparsers.add_parser("search", help="Search prompts.")
    search_parser.add_argument("query")

    show_parser = subparsers.add_parser("show", help="Show one prompt as JSON.")
    show_parser.add_argument("prompt_id")

    render_parser = subparsers.add_parser("render", help="Render a prompt template.")
    render_parser.add_argument("prompt_id")
    render_parser.add_argument("--var", action="append", default=[], help="Template value as key=value.")

    args = parser.parse_args(argv)
    library = PromptLibrary.load(args.library) if args.library else PromptLibrary.load()

    if args.command == "list":
        for prompt in library.all():
            print(f"{prompt.id}\t{prompt.title}")
        return 0
    if args.command == "search":
        for prompt in library.search(args.query):
            print(f"{prompt.id}\t{prompt.title}")
        return 0
    if args.command == "show":
        prompt = library.get(args.prompt_id)
        print(json.dumps(prompt, default=lambda item: item.__dict__, indent=2))
        return 0
    if args.command == "render":
        values = dict(_parse_assignment(item) for item in args.var)
        print(library.get(args.prompt_id).render(**values))
        return 0
    return 1


def _parse_assignment(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("Variables must use key=value syntax")
    key, value = raw.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("Variable key cannot be empty")
    return key, value


if __name__ == "__main__":
    raise SystemExit(main())
