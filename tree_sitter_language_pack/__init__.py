from __future__ import annotations

from importlib import import_module
from typing import Literal, cast

import tree_sitter_c_sharp
import tree_sitter_embedded_template
import tree_sitter_yaml
from tree_sitter import Language, Parser

SupportedLanguage = Literal[
    "actionscript",
    "ada",
    "agda",
    "arduino",
    "asm",
    "astro",
    "bash",
    "beancount",
    "bibtex",
    "bicep",
    "bitbake",
    "c",
    "cairo",
    "capnp",
    "chatito",
    "clarity",
    "clojure",
    "cmake",
    "comment",
    "commonlisp",
    "cpon",
    "cpp",
    "csharp",
    "css",
    "csv",
    "cuda",
    "d",
    "dart",
    "dockerfile",
    "doxygen",
    "dtd",
    "elisp",
    "elixir",
    "elm",
    "embeddedtemplate",
    "erlang",
    "fennel",
    "firrtl",
    "fish",
    "fortran",
    "func",
    "gdscript",
    "gitattributes",
    "gitcommit",
    "gitignore",
    "gleam",
    "glsl",
    "gn",
    "go",
    "gomod",
    "gosum",
    "groovy",
    "gstlaunch",
    "hack",
    "hare",
    "haskell",
    "haxe",
    "hcl",
    "heex",
    "hlsl",
    "html",
    "hyprlang",
    "ispc",
    "janet",
    "java",
    "javascript",
    "jsdoc",
    "json",
    "jsonnet",
    "julia",
    "kconfig",
    "kdl",
    "kotlin",
    "latex",
    "linkerscript",
    "llvm",
    "lua",
    "luadoc",
    "luap",
    "luau",
    "magik",
    "make",
    "markdown",
    "matlab",
    "mermaid",
    "meson",
    "ninja",
    "nix",
    "nqc",
    "objc",
    "odin",
    "org",
    "pascal",
    "pem",
    "perl",
    "pgn",
    "php",
    "po",
    "pony",
    "powershell",
    "printf",
    "prisma",
    "properties",
    "psv",
    "puppet",
    "purescript",
    "pymanifest",
    "python",
    "qmldir",
    "qmljs",
    "query",
    "r",
    "racket",
    "re2c",
    "readline",
    "requirements",
    "ron",
    "rst",
    "ruby",
    "rust",
    "scala",
    "scheme",
    "scss",
    "smali",
    "smithy",
    "solidity",
    "sql",
    "squirrel",
    "starlark",
    "svelte",
    "tablegen",
    "tcl",
    "terraform",
    "test",
    "thrift",
    "toml",
    "tsv",
    "tsx",
    "twig",
    "typescript",
    "typst",
    "udev",
    "ungrammar",
    "uxntal",
    "v",
    "verilog",
    "vhdl",
    "vim",
    "vue",
    "wgsl",
    "xcompose",
    "xml",
    "yaml",
    "yuck",
    "zig",
]


def get_binding(language_name: SupportedLanguage) -> int | object:
    """Get the binding for the given language name.

    Args:
        language_name: The name of the language.

    Raises:
        LookupError: If the language is not found.

    Returns:
        int: The binding for the language.
    """
    if language_name == "yaml":
        return tree_sitter_yaml.language()

    if language_name == "csharp":
        return tree_sitter_c_sharp.language()

    if language_name == "embeddedtemplate":
        return tree_sitter_embedded_template.language()

    try:
        module = import_module(name=f".bindings.{language_name}", package=__package__)
        return cast(int, module.language())
    except ModuleNotFoundError as e:
        raise LookupError(f"Language not found: {language_name}") from e


def get_language(language_name: SupportedLanguage) -> Language:
    """Get the language with the given name.

    Args:
        language_name: The name of the language.

    Returns:
        Language: The language as a tree-sitter Language instance.
    """
    binding = get_binding(language_name)
    return Language(binding)


def get_parser(language_name: SupportedLanguage) -> Parser:
    """Get a parser for the given language name.

    Args:
        language_name: The name of the language.

    Returns:
        Parser: The parser for the language as a tree-sitter Parser instance.
    """
    return Parser(get_language(language_name=language_name))


__all__ = ["SupportedLanguage", "get_binding", "get_language", "get_parser"]
