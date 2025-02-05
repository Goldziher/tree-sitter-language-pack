from __future__ import annotations

from json import loads
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import SupportedLanguage, get_binding, get_language, get_parser

if TYPE_CHECKING:
    from collections.abc import Callable

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
    supported_languages = sorted([*SupportedLanguage.__args__[0].__args__, *SupportedLanguage.__args__[1].__args__])  # type: ignore[attr-defined]
    assert supported_languages == sorted(language_names)


@pytest.mark.parametrize("language", language_names)
def test_get_binding(language: SupportedLanguage) -> None:
    assert isinstance(get_binding(language), int)


@pytest.mark.parametrize("language", language_names)
def test_get_language(language: SupportedLanguage) -> None:
    assert isinstance(get_language(language), Language)


@pytest.mark.parametrize("language", language_names)
def test_get_parser(language: SupportedLanguage) -> None:
    assert isinstance(get_parser(language), Parser)


@pytest.mark.parametrize("handler", [get_language, get_parser])
def test_raises_exception_for_invalid_name(handler: Callable[[str], Any]) -> None:
    with pytest.raises(LookupError):
        handler("invalid")
