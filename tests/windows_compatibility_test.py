from __future__ import annotations

import platform

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import get_language, get_parser


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows specific test")
@pytest.mark.parametrize("language", ["python", "javascript", "typescript", "java"])
def test_import_languages_on_windows(language: str) -> None:
    """Test that languages can be imported correctly on Windows."""
    language_obj = get_language(language)  # type: ignore[arg-type]
    assert language_obj is not None, f"The language {language} could not be loaded"
    assert isinstance(language_obj, Language)

    parser = get_parser(language)  # type: ignore[arg-type]
    assert parser is not None, f"The parser for {language} could not be created"
    assert isinstance(parser, Parser)
