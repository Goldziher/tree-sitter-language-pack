from importlib import import_module
from typing import Callable, Literal, Union, cast

from tree_sitter import Language, Parser
from tree_sitter_c_sharp import language as c_sharp_language
from tree_sitter_embedded_template import language as embedded_template_language
from tree_sitter_yaml import language as yaml_language

InstalledBindings = Literal["csharp", "embeddedtemplate", "yaml"]
SupportedLanguage = Union[
    Literal[
        "agda",
        "arduino",
        "bash",
        "bicep",
        "bitbake",
        "c",
        "cairo",
        "capnp",
        "chatito",
        "clarity",
        "commonlisp",
        "cpp",
        "cpon",
        "css",
        "cuda",
        "csv",
        "doxygen",
        "elixir",
        "elm",
        "firrtl",
        "fortran",
        "func",
        "gitattributes",
        "glsl",
        "go",
        "gomod",
        "gosum",
        "gn",
        "gstlaunch",
        "hack",
        "hare",
        "haskell",
        "hcl",
        "terraform",
        "heex",
        "hlsl",
        "html",
        "hyprlang",
        "ispc",
        "java",
        "javascript",
        "json",
        "jsdoc",
        "julia",
        "kconfig",
        "kdl",
        "linkerscript",
        "lua",
        "luadoc",
        "luap",
        "luau",
        "make",
        "markdown",
        "meson",
        "nqc",
        "objc",
        "ocaml",
        "odin",
        "pem",
        "php",
        "po",
        "pony",
        "printf",
        "properties",
        "puppet",
        "pymanifest",
        "qmljs",
        "qmldir",
        "query",
        "re2c",
        "readline",
        "requirements",
        "ron",
        "ruby",
        "rust",
        "scala",
        "scss",
        "smali",
        "solidity",
        "squirrel",
        "starlark",
        "swift",
        "svelte",
        "tablegen",
        "tcl",
        "test",
        "thrift",
        "toml",
        "typescript",
        "tsx",
        "udev",
        "ungrammar",
        "uxntal",
        "verilog",
        "vim",
        "vue",
        "xml",
        "dtd",
        "xcompose",
        "yuck",
        "wgsl",
        "python",
        "dart",
        "v",
        "matlab",
        "powershell",
        "r",
    ],
    InstalledBindings,
]

installed_bindings_map: dict[InstalledBindings, Callable[[], int]] = {
    "csharp": c_sharp_language,
    "embeddedtemplate": embedded_template_language,
    "yaml": yaml_language,
}


def get_language(language_name: SupportedLanguage) -> Language:
    """Get the language with the given name."""
    if language_name in installed_bindings_map:
        return Language(installed_bindings_map[cast(InstalledBindings, language_name)]())

    try:
        module = import_module(name=f".bindings.{language_name}", package=__package__)
        return Language(module.language())
    except ModuleNotFoundError as e:
        raise LookupError(f"Language not found: {language_name}") from e


def get_parser(language_name: SupportedLanguage) -> Parser:
    """Get a parser for the given language name."""
    return Parser(get_language(language_name=language_name))


__all__ = ["get_language", "get_parser", "SupportedLanguage"]
