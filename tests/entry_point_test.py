from collections.abc import Callable
from json import loads
from pathlib import Path
from typing import Any, cast

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import SupportedLanguage, get_language, get_parser

language_definitions = cast(
    dict[str, dict[str, str]],
    loads((Path(__file__).parent.parent.resolve() / "sources" / "language_definitions.json").read_text()),
)
language_names = [
    *list(language_definitions.keys()),
    "csharp",
    "embeddedtemplate",
    "yaml",
    "typescript",
    "tsx",
    "xml",
    "php",
    "dtd",
]


def test_language_names() -> None:
    supported_langauges = sorted([*SupportedLanguage.__args__[0].__args__, *SupportedLanguage.__args__[1].__args__])  # type: ignore[attr-defined]
    assert supported_langauges == sorted(language_names)


@pytest.mark.parametrize("language", language_names)
def test_get_language(language: SupportedLanguage) -> None:
    assert isinstance(get_language(language), Language)


@pytest.mark.parametrize("language", language_names)
def test_get_parser(language: SupportedLanguage) -> None:
    assert isinstance(get_parser(language), Parser)


@pytest.mark.parametrize("handler", (get_language, get_parser))
def test_raises_exception_for_invalid_name(handler: Callable[[str], Any]) -> None:
    with pytest.raises(LookupError):
        handler("invalid")
