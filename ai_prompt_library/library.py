"""Prompt catalog loading, search, rendering, and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from string import Formatter
from typing import Iterable

_DEFAULT_LIBRARY_PATH = Path(__file__).resolve().parents[1] / "prompts" / "library.json"
_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True)
class PromptVariable:
    """A variable accepted by a prompt template."""

    name: str
    description: str
    example: str = ""
    required: bool = True


@dataclass(frozen=True)
class Prompt:
    """A single prompt entry in the catalog."""

    id: str
    title: str
    category: str
    description: str
    tags: tuple[str, ...]
    variables: tuple[PromptVariable, ...]
    template: str
    best_practices: tuple[str, ...]

    @property
    def variable_names(self) -> set[str]:
        return {variable.name for variable in self.variables}

    @property
    def template_fields(self) -> set[str]:
        return {
            field_name
            for _, field_name, _, _ in Formatter().parse(self.template)
            if field_name
        }

    def render(self, **values: str) -> str:
        """Render the prompt template with supplied values."""
        missing = sorted(self.template_fields - values.keys())
        if missing:
            raise ValueError(f"Missing template values for: {', '.join(missing)}")
        return self.template.format(**values)


class PromptLibrary:
    """In-memory prompt catalog with validation and search helpers."""

    def __init__(self, prompts: Iterable[Prompt]):
        self._prompts = tuple(prompts)
        self._by_id = {prompt.id: prompt for prompt in self._prompts}
        if len(self._by_id) != len(self._prompts):
            raise ValueError("Prompt ids must be unique")

    @classmethod
    def load(cls, path: str | Path = _DEFAULT_LIBRARY_PATH) -> "PromptLibrary":
        with Path(path).open(encoding="utf-8") as prompt_file:
            raw_prompts = json.load(prompt_file)
        return cls(_parse_prompt(item) for item in raw_prompts)

    def all(self) -> tuple[Prompt, ...]:
        return self._prompts

    def get(self, prompt_id: str) -> Prompt:
        try:
            return self._by_id[prompt_id]
        except KeyError as exc:
            raise KeyError(f"Unknown prompt id: {prompt_id}") from exc

    def search(self, query: str) -> tuple[Prompt, ...]:
        normalized = query.casefold().strip()
        if not normalized:
            return self.all()
        return tuple(
            prompt
            for prompt in self._prompts
            if normalized in _search_blob(prompt)
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        seen_ids: set[str] = set()
        for index, prompt in enumerate(self._prompts):
            location = f"prompt[{index}] ({prompt.id})"
            if not _ID_PATTERN.match(prompt.id):
                errors.append(f"{location}: id must be snake_case and start with a letter")
            if prompt.id in seen_ids:
                errors.append(f"{location}: duplicate id")
            seen_ids.add(prompt.id)
            if not prompt.title.strip():
                errors.append(f"{location}: title is required")
            if not prompt.template.strip():
                errors.append(f"{location}: template is required")
            undefined_fields = prompt.template_fields - prompt.variable_names
            unused_variables = prompt.variable_names - prompt.template_fields
            if undefined_fields:
                errors.append(f"{location}: template fields are not declared: {sorted(undefined_fields)}")
            if unused_variables:
                errors.append(f"{location}: variables are not used by template: {sorted(unused_variables)}")
        return errors


def _parse_prompt(raw: dict) -> Prompt:
    return Prompt(
        id=raw["id"],
        title=raw["title"],
        category=raw["category"],
        description=raw["description"],
        tags=tuple(raw.get("tags", [])),
        variables=tuple(PromptVariable(**variable) for variable in raw.get("variables", [])),
        template=raw["template"],
        best_practices=tuple(raw.get("best_practices", [])),
    )


def _search_blob(prompt: Prompt) -> str:
    return " ".join(
        [prompt.id, prompt.title, prompt.category, prompt.description, *prompt.tags]
    ).casefold()
