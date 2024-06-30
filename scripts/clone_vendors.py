import subprocess
from json import loads
from pathlib import Path
from shutil import move
from typing import Optional

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


def clone_repository(repo_url: str, branch: Optional[str], language_name: str) -> None:
    """Clone a repository.

    Args:
        repo_url (str): The repository URL.
        branch (str | None): The branch to clone.
        language_name (str): The name of the repository.

    Returns:
        Repo: The cloned repository.
    """
    print(f"Cloning {repo_url}")
    repo = Repo.clone_from(url=repo_url, to_path=vendor_directory / language_name)
    if branch and branch != repo.active_branch:
        print(f"Checking out branch {branch}")
        repo.git.checkout(branch)
    print(f"Cloned {repo_url} successfully")


def handle_generate(language_name: str, directory: Optional[str]) -> None:
    """Handle the generation of a language.

    Args:
        language_name (str): The name of the language.
        directory (str | None): The directory to generate the language in.

    Returns:
        None
    """
    print(f"Generating {language_name} using tree-sitter-cli")
    target_dir = (
        (vendor_directory / language_name / directory).resolve()
        if directory
        else (vendor_directory / language_name).resolve()
    )
    subprocess.run(["tree-sitter", "generate"], cwd=str(target_dir), check=False)
    print(f"Generated {language_name} parser successfully")


def move_src_folder(language_name: str, directory: Optional[str]) -> None:
    """Move the src folder to the parsers directory.

    Args:
        language_name (str): The name of the language.
        directory (str | None): The directory to move the src folder from.

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
    target_dir.mkdir(parents=True, exist_ok=True)
    move(source_dir, target_dir)
    print(f"Moved {language_name} parser files successfully")


if __name__ == "__main__":
    language_definitions, language_names = get_language_definitions()
    for language_name, language_definition in language_definitions.items():
        clone_repository(
            repo_url=language_definition["repo"], branch=language_definition.get("branch"), language_name=language_name
        )
        if language_definition.get("generate", False):
            handle_generate(language_name=language_name, directory=language_definition.get("directory"))
        move_src_folder(language_name=language_name, directory=language_definition.get("directory"))
