from __future__ import annotations

import platform

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import get_language, get_parser

# Languages to test
languages_to_test = ["python", "javascript", "typescript", "java"]


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows specific test")
@pytest.mark.parametrize("language", languages_to_test)
def test_import_languages_on_windows(language: str) -> None:
    """Test that languages can be imported correctly on Windows."""
    # Test language loading
    language_obj = get_language(language)
    assert language_obj is not None, f"The language {language} could not be loaded"
    assert isinstance(language_obj, Language)

    # Test parser creation
    parser = get_parser(language)
    assert parser is not None, f"The parser for {language} could not be created"
    assert isinstance(parser, Parser)