from __future__ import annotations

import asyncio
import os
import platform
import re
import sys
from json import loads
from pathlib import Path
from shutil import move, rmtree, which

from anyio import Path as AsyncPath
from anyio import run_process
from anyio.to_thread import run_sync
from typing_extensions import NotRequired, TypedDict

vendor_directory = Path(__file__).parent.parent / "vendor"
parsers_directory = Path(__file__).parent.parent / "parsers"

# Use raw string with escaped forward slashes to work across platforms
COMMON_RE_PATTERN = re.compile(r"\.\.[/\\](?:\.\.[/\\])*common[/\\]")


class LanguageDict(TypedDict):
    """Language configuration for tree-sitter repositories."""

    directory: NotRequired[str]
    generate: NotRequired[bool]
    rewrite_targets: NotRequired[bool]
    abi_version: NotRequired[int]


def get_language_definitions() -> tuple[dict[str, LanguageDict], list[str]]:
    """Get the language definitions."""
    print("Loading language definitions")
    language_definitions: dict[str, LanguageDict] = loads(
        (Path(__file__).parent.parent / "sources" / "language_definitions.json").read_text()
    )
    # return a list of language names
    language_names = list(language_definitions.keys())
    return language_definitions, language_names


async def handle_generate(language_name: str, directory: str | None, abi_version: int) -> None:
    """Handle the generation of a language.

    Args:
        language_name: The name of the language.
        directory: The directory to generate the language in.
        abi_version: The ABI version to use.

    Raises:
        RuntimeError: if generate fails.

    Returns:
        None
    """
    print(f"Generating {language_name} using tree-sitter-cli")
    target_dir = (
        (vendor_directory / language_name / directory).resolve()
        if directory
        else (vendor_directory / language_name).resolve()
    )

    if platform.system() == "Windows":
        cmd = ["cmd", "/c", "tree-sitter", "generate", "--abi", str(abi_version)]
    else:
        cmd = ["tree-sitter", "generate", "--abi", str(abi_version)]

    try:
        await run_process(cmd, cwd=str(target_dir), check=False)
        print(f"Generated {language_name} parser successfully")
    except Exception as e:
        raise RuntimeError(f"failed to clone {language_name} due to an exception: {e}") from e


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
    target_source_dir = (parsers_directory / language_name).resolve()
    await AsyncPath(target_source_dir).mkdir(parents=True, exist_ok=True)
    await run_sync(move, source_dir, target_source_dir)
    print(f"Moved {language_name} parser files successfully")

    common_source_dir = vendor_directory / language_name / "common"

    if await AsyncPath(common_source_dir).exists():
        print(f"Moving {language_name} common files")
        await run_sync(move, common_source_dir, target_source_dir)
        print(f"Moved {language_name} common files successfully")

        for file in target_source_dir.glob("**/*.c"):
            # replace any include statement that points at common with an updated path:
            # e.g. '#include "../../common/scanner.h"' should point at (target_common_dir / 'scanner.h').relative_path()
            file_contents = await AsyncPath(file).read_text()

            # Create a properly formatted replacement path with the correct path separator
            replacement_path = os.path.relpath(target_source_dir / "common", file.parent)
            # Ensure forward slashes in replacement path for C includes (even on Windows)
            replacement_path = replacement_path.replace("\\", "/") + "/"

            file_contents = COMMON_RE_PATTERN.sub(replacement_path, file_contents)
            await AsyncPath(file).write_text(file_contents)


async def process_repo(language_name: str, language_definition: LanguageDict) -> None:
    """Process a repository.

    Args:
        language_name: The name of the language.
        language_definition: The language definition.

    Returns:
        None
    """
    if language_definition.get("generate", False):
        await handle_generate(
            language_name=language_name,
            directory=language_definition.get("directory"),
            abi_version=language_definition.get("abi_version", 14),
        )
    await move_src_folder(language_name=language_name, directory=language_definition.get("directory"))


async def main() -> None:
    """Main function."""
    parsers_directory.mkdir(exist_ok=True, parents=True)

    language_definitions, language_names = get_language_definitions()

    # Check if submodule directories exist and are initialized
    print("Checking vendor submodules...")
    all_submodules_initialized = True
    for lang_name in language_names:
        submodule_path = vendor_directory / lang_name
        if not submodule_path.is_dir() or not list(Path(submodule_path).iterdir()):
            print(
                f"Error: Submodule for '{lang_name}' not found or not initialized in '{submodule_path}'.",
                file=sys.stderr,
            )
            all_submodules_initialized = False

    if not all_submodules_initialized:
        print(
            "\nPlease initialize/update the submodules using:",
            file=sys.stderr,
        )
        print("  git submodule update --init --recursive", file=sys.stderr)
        sys.exit(1)
    print("All vendor submodules appear to be initialized.")

    await asyncio.gather(
        *[
            process_repo(
                language_name=language_name,
                language_definition=language_definitions[language_name],
            )
            for language_name in language_names
        ]
    )


if __name__ == "__main__":
    if not which("tree-sitter"):
        sys.exit("tree-sitter is a required system dependency. Please install it with 'npm i -g tree-sitter-cli'")

    if parsers_directory.exists():
        print("parsers directory already exists, removing")
        rmtree(parsers_directory)

    asyncio.run(main())
