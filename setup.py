from os import environ, getcwd, listdir
from pathlib import Path
from platform import system
from typing import Any

from setuptools import Extension, find_packages, setup  # type: ignore[import-untyped]
from setuptools.command.build_ext import build_ext  # type: ignore[import-untyped]
from typing_extensions import NotRequired, TypedDict
from wheel.bdist_wheel import bdist_wheel  # type: ignore[import-untyped]


class LanguageDict(TypedDict):
    """Language configuration for tree-sitter repositories."""

    repo: str
    branch: NotRequired[str]
    directory: NotRequired[str]
    generate: NotRequired[bool]


def get_mapped_parsers() -> dict[str, Path]:
    """Get the language definitions."""
    parsers_dir = Path(environ.get("PROJECT_ROOT", getcwd())).resolve() / "parsers"
    return {dir_name: (parsers_dir / dir_name) for dir_name in listdir(parsers_dir)}


def create_extension(*, language_name: str) -> Extension:
    """Create an extension for the given language.

    Args:
        language_name (str): The name of the language.

    Returns:
        Extension: The extension for the language.
    """
    compile_args = (
        [
            "-Werror=implicit-function-declaration",
            "-Wno-cast-function-type",
            "-Wno-unused-but-set-variable",
            "-fvisibility=hidden",
            "-std=c11",
        ]
        if system() != "Windows"
        else [
            "/std:c11",
            "/wd4244",
        ]
    )

    return Extension(
        name=f"tree_sitter_language_pack.bindings.{language_name}",
        py_limited_api=True,
        define_macros=[
            ("PY_SSIZE_T_CLEAN", None),
            ("TREE_SITTER_HIDE_SYMBOLS", None),
            ("TS_LANGUAGE_NAME", language_name),
        ],
        extra_compile_args=compile_args,
        sources=[],
    )


mapped_parsers = get_mapped_parsers()
# Create extensions for all languages defined in the JSON file
extensions = [create_extension(language_name=language_name) for language_name in mapped_parsers]


class BuildExt(build_ext):  # type: ignore[misc]
    """Custom build extension to handle tree-sitter language repositories."""

    def build_extension(self, ext: Extension) -> None:
        """Build the extension."""
        language_name = ext.name.split(".")[-1]
        cwd = Path(getcwd())

        # Add the language extension source file
        language_extension = (cwd / "sources" / "language_extension.c").resolve()
        if not language_extension.is_file():
            raise FileNotFoundError(f"Language extension file not found: {language_extension}")
        ext.sources = [str(language_extension.relative_to(cwd))]

        parser_dir = mapped_parsers[language_name]

        # Set up vendor sources for building the extension
        parser_src_dir = parser_dir / "src"
        ext.include_dirs = [str(parser_src_dir)]
        ext.sources.extend([str(src_file_path.relative_to(cwd)) for src_file_path in parser_src_dir.glob("*.c")])

        super().build_extension(ext)


class BdistWheel(bdist_wheel):  # type: ignore[misc]
    """Custom bdist_wheel command to handle Python 3.9 ABI tag."""

    def get_tag(self) -> tuple[Any, Any, Any]:
        """Get the tag for the wheel distribution."""
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp39", "abi3"
        return python, abi, platform


setup(
    packages=find_packages(include=["tree_sitter_language_pack", "tree_sitter_language_pack.bindings"]),
    package_data={"tree_sitter_language_pack": ["py.typed"], "tree_sitter_language_pack.bindings": ["*.so"]},
    ext_modules=extensions,
    include_package_data=True,
    cmdclass={
        "build_ext": BuildExt,
        "bdist_wheel": BdistWheel,
    },
    options={"build_ext": {"inplace": True}},
)
