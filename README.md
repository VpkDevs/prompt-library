# AI Prompt Library

A curated, versioned prompt library for common AI workflows. The repository includes:

- A structured prompt catalog in JSON.
- A Python package for loading, searching, rendering, and validating prompts.
- A small CLI for discovery and templating.
- Tests and contributor documentation to keep prompts high quality.

## Quick start

```bash
python -m ai_prompt_library list
python -m ai_prompt_library show summarize_meeting
python -m ai_prompt_library render summarize_meeting --var audience="executives" --var transcript="..."
```

## Prompt format

Prompts live in [`prompts/library.json`](prompts/library.json). Each prompt includes:

- `id`: stable snake_case identifier
- `title`: human-readable name
- `category`: workflow area
- `description`: short summary
- `tags`: searchable keywords
- `variables`: template inputs with descriptions and examples
- `template`: prompt text using `{variable}` placeholders
- `best_practices`: usage guidance

## Development

```bash
python -m pytest
python scripts/validate_prompts.py
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution standards.
