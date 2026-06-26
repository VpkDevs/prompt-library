from ai_prompt_library import PromptLibrary


def test_default_library_is_valid():
    assert PromptLibrary.load().validate() == []


def test_search_matches_tags_and_descriptions():
    library = PromptLibrary.load()
    assert [prompt.id for prompt in library.search("security")] == ["code_review"]
    assert [prompt.id for prompt in library.search("meeting")] == ["summarize_meeting"]


def test_render_requires_declared_template_values():
    prompt = PromptLibrary.load().get("summarize_meeting")
    rendered = prompt.render(audience="leaders", transcript="We shipped the release.")
    assert "leaders" in rendered
    assert "We shipped the release." in rendered


def test_render_reports_missing_values():
    prompt = PromptLibrary.load().get("code_review")
    try:
        prompt.render(language="Python")
    except ValueError as error:
        assert "diff" in str(error)
    else:
        raise AssertionError("render should fail when a template value is missing")
