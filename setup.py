from itertools import chain
from os import environ, getcwd, listdir
from pathlib import Path
from platform import system

from setuptools import Extension, find_packages, setup
from setuptools.command.bdist_wheel import bdist_wheel
from setuptools.command.build_ext import build_ext

MIN_PYTHON_VERSION = 39


def get_mapped_parsers() -> dict[str, Path]:
    """Get the language definitions."""
    parsers_dir = Path(environ.get("PROJECT_ROOT", getcwd())).resolve() / "parsers"  # noqa: PTH109
    return {dir_name: (parsers_dir / dir_name) for dir_name in listdir(parsers_dir)}  # noqa: PTH208


def create_extension(*, language_name: str) -> Extension:
    """Create an extension for the given language.

    Args:
        language_name: The name of the language.

    Returns:
        Extension: The extension for the language.
    """
    compile_args = (
        [
            "-fvisibility=hidden",
            "-std=c11",
        ]
        if system() != "Windows"
        else [
            "/std:c11",
            "/utf-8",
            "/wd4244",  # Suppress warnings about integer type conversion
            "/wd4566",  # Suppress warnings about character representation
            "/wd4819",  # Suppress warnings about source files with encoding issues
        ]
    )

    define_macros = [
        ("PY_SSIZE_T_CLEAN", None),
        ("TREE_SITTER_HIDE_SYMBOLS", None),
        ("TS_LANGUAGE_NAME", language_name),
    ]

    if system() == "Windows":
        define_macros.append(("Py_LIMITED_API", "0x03090000"))  # Python 3.9+

    return Extension(
        name=f"tree_sitter_language_pack.bindings.{language_name}",
        py_limited_api=True,
        define_macros=define_macros,
        extra_compile_args=compile_args,
        sources=[],
    )


# Get the mapped parsers
mapped_parsers = get_mapped_parsers()
# Create extensions for all languages defined in the JSON file
extensions = [create_extension(language_name=language_name) for language_name in mapped_parsers]
# Add the data files for the parsers
data_files = [
    str(value)
    for value in chain.from_iterable(list(parser_dir.iterdir()) for parser_dir in mapped_parsers.values())
    if value.is_file()
]


class BuildExt(build_ext):
    """Custom build extension to handle tree-sitter language repositories."""

    def build_extension(self, ext: Extension) -> None:
        """Build the extension."""
        language_name = ext.name.split(".")[-1]
        cwd = Path(getcwd())  # noqa: PTH109

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


class BdistWheel(bdist_wheel):
    """Custom bdist_wheel command to handle Python 3.9+ ABI tag."""

    def get_tag(self) -> tuple[str, str, str]:
        """Get the tag for the wheel."""
        python, abi, platform = super().get_tag()
        platform = platform.replace("linux", "manylinux2014")
        if python.startswith("cp") and int(python[2:]) >= MIN_PYTHON_VERSION:
            # Support all Python versions >= 3.9 using abi3
            return "cp39", "abi3", platform
        return python, abi, platform


setup(
    packages=find_packages(include=["tree_sitter_language_pack", "tree_sitter_language_pack.bindings"]),
    package_data={"tree_sitter_language_pack": ["py.typed"]},
    data_files=[("parsers", data_files)],
    ext_modules=extensions,
    include_package_data=True,
    cmdclass={
        "build_ext": BuildExt,
        "bdist_wheel": BdistWheel,
    },
    options={"build_ext": {"inplace": True}},
)
