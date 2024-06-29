from collections.abc import Callable
from json import loads
from pathlib import Path
from typing import Any, cast

import pytest
from tree_sitter import Language, Parser

from tree_sitter_language_pack import SupportedLanguage, get_language, get_parser

language_definition_list = cast(
    list[dict[str, str]],
    loads((Path(__file__).parent.parent.resolve() / "sources" / "language_definitions.json").read_text()),
)
language_names = [
    language_definition.get("directory", language_definition["repo"])
    .split("/")[-1]
    .replace("tree-sitter-", "")
    .replace(
        "-",
        "",
    )
    for language_definition in language_definition_list
] + ["csharp", "embeddedtemplate", "yaml"]


def test_language_names() -> None:
    assert sorted([*SupportedLanguage.__args__[0].__args__, *SupportedLanguage.__args__[1].__args__]) == sorted(  # type: ignore[attr-defined]
        language_names
    )


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
