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
        "cpon",
        "cpp",
        "css",
        "csv",
        "cuda",
        "doxygen",
        "dtd",
        "elixir",
        "elm",
        "firrtl",
        "fortran",
        "func",
        "gitattributes",
        "glsl",
        "gn",
        "go",
        "gomod",
        "gosum",
        "gstlaunch",
        "hack",
        "hare",
        "haskell",
        "hcl",
        "heex",
        "hlsl",
        "html",
        "hyprlang",
        "ispc",
        "java",
        "javascript",
        "jsdoc",
        "json",
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
        "qmldir",
        "qmljs",
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
        "svelte",
        "swift",
        "tablegen",
        "tcl",
        "terraform",
        "test",
        "thrift",
        "toml",
        "tsx",
        "typescript",
        "udev",
        "ungrammar",
        "uxntal",
        "verilog",
        "vim",
        "vue",
        "wgsl",
        "xcompose",
        "xml",
        "yuck",
    ],
    InstalledBindings,
]

installed_bindings_map: dict[InstalledBindings, Callable[[], int]] = {
    "csharp": c_sharp_language,
    "embeddedtemplate": embedded_template_language,
    "yaml": yaml_language,
}


def get_language(name: SupportedLanguage) -> Language:
    """Get the language with the given name."""
    if name in installed_bindings_map:
        return Language(installed_bindings_map[cast(InstalledBindings, name)]())

    try:
        module = import_module(name=f".languages.{name}", package=__package__)
        return Language(module.language())
    except ModuleNotFoundError as e:
        raise LookupError(f"Language not found: {name}") from e


def get_parser(name: SupportedLanguage) -> Parser:
    """Get a parser for the given language name."""
    return Parser(get_language(name))


__all__ = ["get_language", "get_parser", "SupportedLanguage"]
