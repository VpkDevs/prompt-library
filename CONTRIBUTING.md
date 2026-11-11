# Contributing

Thank you for improving the AI Prompt Library.

## Adding or updating prompts

1. Edit `prompts/library.json`.
2. Use stable, snake_case prompt IDs.
3. Declare every `{variable}` used in the template.
4. Include practical `best_practices` that help users avoid misuse.
5. Run the validation and test commands before opening a pull request.

```bash
python scripts/validate_prompts.py
python -m pytest
```

## Quality bar

A prompt should be specific about role, inputs, output structure, constraints, and quality criteria. Avoid prompts that encourage fabricating facts, hiding uncertainty, or collecting sensitive data unnecessarily.
