from __future__ import annotations

import asyncio
import subprocess
from functools import partial
from json import loads
from pathlib import Path
from shutil import move

from anyio.to_thread import run_sync
from git import Repo
from typing_extensions import NotRequired, TypedDict

vendor_directory = Path(__file__).parent.parent / "vendor"
parsers_directory = Path(__file__).parent.parent / "parsers"


class LanguageDict(TypedDict):
    """Language configuration for tree-sitter repositories."""

    repo: str
    branch: NotRequired[str]
    directory: NotRequired[str]
    generate: NotRequired[bool]


def get_language_definitions() -> tuple[dict[str, LanguageDict], list[str]]:
    """Get the language definitions."""
    print("Loading language definitions")
    language_definitions: dict[str, LanguageDict] = loads(
        (Path(__file__).parent.parent / "sources" / "language_definitions.json").read_text()
    )
    # return a list of language names
    language_names = list(language_definitions.keys())
    return language_definitions, language_names


async def clone_repository(repo_url: str, branch: str | None, language_name: str) -> None:
    """Clone a repository.

    Args:
        repo_url: The repository URL.
        branch: The branch to clone.
        language_name: The name of the repository.

    Returns:
        Repo: The cloned repository.
    """
    print(f"Cloning {repo_url}")
    kwargs = {"url": repo_url, "to_path": vendor_directory / language_name, "depth": 1}
    if branch:
        kwargs["branch"] = branch
    handler = partial(Repo.clone_from, **kwargs)  # type: ignore[arg-type]

    await run_sync(handler)
    print(f"Cloned {repo_url} successfully")


async def handle_generate(language_name: str, directory: str | None) -> None:
    """Handle the generation of a language.

    Args:
        language_name: The name of the language.
        directory: The directory to generate the language in.

    Returns:
        None
    """
    print(f"Generating {language_name} using tree-sitter-cli")
    target_dir = (
        (vendor_directory / language_name / directory).resolve()
        if directory
        else (vendor_directory / language_name).resolve()
    )
    await run_sync(partial(subprocess.run, ["tree-sitter", "generate"], cwd=str(target_dir), check=False))
    print(f"Generated {language_name} parser successfully")


async def move_src_folder(language_name: str, directory: str | None) -> None:
    """Move the src folder to the parsers directory.

    Args:
        language_name: The name of the language.
        directory: The directory to move the src folder from.

    Returns:
        None
    """
    print(f"Moving {language_name} parser files")
    source_dir = (
        (vendor_directory / language_name / directory / "src").resolve()
        if directory
        else (vendor_directory / language_name / "src").resolve()
    )
    target_dir = (parsers_directory / language_name).resolve()
    await run_sync(partial(target_dir.mkdir, parents=True, exist_ok=True))
    await run_sync(move, source_dir, target_dir)
    print(f"Moved {language_name} parser files successfully")


async def process_repo(language_name: str, language_definition: LanguageDict) -> None:
    """Process a repository.

    Args:
        language_name: The name of the language.
        language_definition: The language definition.

    Returns:
        None
    """
    await clone_repository(
        repo_url=language_definition["repo"], branch=language_definition.get("branch"), language_name=language_name
    )
    if language_definition.get("generate", False):
        await handle_generate(language_name=language_name, directory=language_definition.get("directory"))
    await move_src_folder(language_name=language_name, directory=language_definition.get("directory"))


async def main() -> None:
    """Main function."""
    language_definitions, language_names = get_language_definitions()
    await asyncio.gather(
        *[
            process_repo(language_name=language_name, language_definition=language_definitions[language_name])
            for language_name in language_names
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
