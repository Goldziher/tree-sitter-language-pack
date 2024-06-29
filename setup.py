from json import loads
from os import chdir, environ, getcwd
from pathlib import Path
from platform import system
from typing import Any, Optional

from setuptools import Extension, find_packages, setup  # type: ignore[import-untyped]
from setuptools.command.build_ext import build_ext  # type: ignore[import-untyped]
from typing_extensions import NotRequired, TypedDict
from wheel.bdist_wheel import bdist_wheel  # type: ignore[import-untyped]


class LanguageDict(TypedDict):
    """Language configuration for tree-sitter repositories."""

    repo: str
    branch: NotRequired[str]
    directory: NotRequired[str]
    cmd: NotRequired[list[str]]


def get_language_definitions() -> tuple[dict[str, LanguageDict], list[str]]:
    """Get the language definitions."""
    project_root = Path(environ.get("PROJECT_ROOT", getcwd()))

    # Load language configurations from a JSON file
    language_definition_list: list[LanguageDict] = loads((project_root / "language_definitions.json").read_text())
    # create PascalCase identifiers from the package names
    language_names = [
        language_definition.get("directory", language_definition["repo"])
        .split("/")[-1]
        .replace("tree-sitter-", "")
        .replace(
            "-",
            "",
        )
        for language_definition in language_definition_list
    ]
    # Create a dictionary of language definitions mapped to the language names
    language_definitions = dict(zip(language_names, language_definition_list))
    return language_definitions, language_names


def create_extension(*, language_name: str) -> Extension:
    """Create an extension for the given language.

    Args:
        language_name (str): The name of the language.

    Returns:
        Extension: The extension for the language.
    """
    return Extension(
        name=f"tree_sitter_language_pack.languages.{language_name}",
        sources=["language_extension.c"],
        include_dirs=[language_name],
        define_macros=[
            ("PY_SSIZE_T_CLEAN", None),
            ("TREE_SITTER_HIDE_SYMBOLS", None),
            ("TS_LANGUAGE_NAME", language_name),
        ],
        extra_compile_args=[
            "-std=c11",
            "-fvisibility=hidden",
            "-Wno-cast-function-type",
            "-Wno-unused-but-set-variable",
            "-Werror=implicit-function-declaration",
        ]
        if system() != "Windows"
        else [
            "/std:c11",
            "/wd4244",
        ],
        py_limited_api=True,
        optional=True,
    )


# Get the language definitions and names from the JSON file
language_definitions, language_names = get_language_definitions()
# Create extensions for all languages defined in the JSON file
extensions = [create_extension(language_name=language_name) for language_name in language_names]


class BuildExt(build_ext):  # type: ignore[misc]
    """Custom build extension to handle tree-sitter language repositories."""

    def build_extension(self, ext: Extension) -> None:
        """Build the extension."""
        extension_dir_name = ext.include_dirs.pop()
        language_name = ext.name.split(".")[-1]
        language_definition = language_definitions[language_name]
        cwd = Path(getcwd())

        directory = cwd / "vendor" / extension_dir_name
        relative_path = directory.relative_to(cwd)

        # Clone or pull the language repository
        if directory.is_dir():
            self.update_repo(directory=str(relative_path))
        else:
            self.clone_repo(
                repo=language_definition["repo"], branch=language_definition.get("branch"), directory=str(relative_path)
            )

        # Run the command to build the language if provided
        if cmd := language_definition.get("cmd"):
            chdir(directory)
            self.spawn(cmd)
            chdir(cwd)

        # Set up paths for building the extension
        source_dir = directory / language_definition.get("directory", "") / "src"
        ext.sources.extend([str(src_file) for src_file in source_dir.glob("*.c")])
        ext.include_dirs = [str(source_dir)]

        super().build_extension(ext)

    def update_repo(self, directory: str) -> None:
        """Update a repository.

        Args:
            directory (str): The directory of the repository to update.

        Returns:
            None
        """
        self.spawn(["git", "-C", directory, "pull", "-q", "--depth=1"])

    def clone_repo(self, repo: str, branch: Optional[str], directory: str) -> None:
        """Clone a repository.

        Args:
            repo (str): The repository URL.
            branch (Optional[str]): The branch to clone.
            directory (str): The directory to clone the repository to.

        Returns:
            None
        """
        clone_cmd = [
            "git",
            "clone",
            "-q",
            "--depth=1",
        ]
        if branch:
            clone_cmd.append(f"--branch={branch}")

        self.spawn(
            [
                *clone_cmd,
                repo,
                directory,
            ]
        )


class BdistWheel(bdist_wheel):  # type: ignore[misc]
    """Custom bdist_wheel command to handle Python 3.9 ABI tag."""

    def get_tag(self) -> tuple[Any, Any, Any]:
        """Get the tag for the wheel distribution."""
        python, abi, platform = super().get_tag()
        if python.startswith("cp"):
            python, abi = "cp39", "abi3"
        return python, abi, platform


setup(
    packages=find_packages(),
    package_data={"tree_sitter_language_pack": ["py.typed"]},
    ext_modules=extensions,
    include_package_data=True,
    cmdclass={
        "build_ext": BuildExt,
        "bdist_wheel": BdistWheel,
    },
)
