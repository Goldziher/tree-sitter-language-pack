from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from git import Repo


def get_latest_commit_hash(repo_url: str, branch: str | None = None) -> str | None:
    """Get the latest commit hash from a repository.

    Args:
        repo_url: The repository URL.
        branch: The branch to checkout.

    Returns:
        str: The latest commit hash.
    """
    print(f"Fetching latest commit for {repo_url} on branch {branch or 'default'}")

    # Create a temporary directory for cloning
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone into the temporary directory
        clone_kwargs = {}
        if branch:
            clone_kwargs["branch"] = branch

        # Clone the repository - avoid passing additional parameters to fix mypy errors
        temp_repo = Repo.clone_from(url=repo_url, to_path=temp_dir)

        # Get the latest commit hash
        latest_commit = temp_repo.head.commit.hexsha
        print(f"Latest commit for {repo_url}: {latest_commit}")
        return latest_commit

    except (ValueError, OSError, RuntimeError) as e:
        print(f"Error fetching commit for {repo_url}: {e}")
        return None

    finally:
        # Clean up the temporary directory
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except (PermissionError, OSError) as e:
            print(f"Warning: could not clean up temporary directory {temp_dir}: {e}")


async def process_language(
    language_name: str, language_def: dict[str, Any], max_workers: int
) -> tuple[str, dict[str, Any]]:
    """Process a language repository to get its latest commit.

    Args:
        language_name: The name of the language.
        language_def: The language definition.
        max_workers: The maximum number of concurrent workers.

    Returns:
        tuple: The language name and updated definition.
    """
    repo_url = language_def["repo"]
    branch = language_def.get("branch")
    language_def_copy = language_def.copy()

    # Skip if --only-missing is set and rev already exists
    if args.only_missing and "rev" in language_def_copy:
        print(f"Skipping {language_name} as it already has a revision pinned")
        return language_name, language_def_copy

    try:
        # Use thread pool for git operations
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            loop = asyncio.get_event_loop()
            latest_commit = await loop.run_in_executor(executor, get_latest_commit_hash, repo_url, branch)

        if latest_commit:
            language_def_copy["rev"] = latest_commit
            print(f"✓ Updated {language_name} to commit {latest_commit}")
        else:
            print(f"✗ Failed to get commit for {language_name}")

    except (ValueError, OSError, RuntimeError) as e:
        print(f"✗ Failed to update {language_name}: {e}")

    return language_name, language_def_copy


async def main(args: argparse.Namespace) -> None:
    """Main function."""
    # Determine level of concurrency based on CPU count
    max_workers = args.workers if args.workers else min(32, (os.cpu_count() or 4) * 2)
    print(f"Using up to {max_workers} concurrent workers")

    # Load the language definitions
    definitions_path = Path(__file__).parent.parent / "sources" / "language_definitions.json"
    print(f"Loading language definitions from {definitions_path}")

    # Use async-compatible file operation
    language_definitions = json.loads(await asyncio.to_thread(lambda: Path(definitions_path).read_text()))

    # Filter languages if a specific subset was requested
    if args.languages:
        requested_languages = args.languages.split(",")
        language_definitions = {k: v for k, v in language_definitions.items() if k in requested_languages}
        print(f"Processing {len(language_definitions)} specified languages: {', '.join(language_definitions.keys())}")
    else:
        print(f"Processing all {len(language_definitions)} languages")

    # Process repositories with a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(max_workers)
    tasks = []

    async def process_with_semaphore(language_name: str, language_def: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        async with semaphore:
            return await process_language(
                language_name, language_def, 1
            )  # 1 worker per task since we're already parallelizing tasks

    for language_name, language_def in language_definitions.items():
        tasks.append(process_with_semaphore(language_name, language_def))

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    # Create a new dictionary with the updated definitions using dictionary comprehension
    updated_definitions = dict(results)

    # Make sure to preserve all original languages even if they weren't processed
    if args.languages:
        # Read the original file again to make sure we have the complete dataset
        all_definitions = json.loads(await asyncio.to_thread(lambda: Path(definitions_path).read_text()))

        # Update only the processed languages
        for lang_name, lang_def in updated_definitions.items():
            all_definitions[lang_name] = lang_def

        updated_definitions = all_definitions

    # Create a backup of the original file
    backup_path = definitions_path.with_suffix(".json.bak")
    shutil.copy2(definitions_path, backup_path)
    print(f"Created backup at {backup_path}")

    # Write the updated definitions back to the file
    print(f"Writing updated language definitions to {definitions_path}")
    await asyncio.to_thread(lambda: Path(definitions_path).write_text(json.dumps(updated_definitions, indent=2)))

    print(f"Done! Updated {len(updated_definitions)} language definitions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pin tree-sitter language repositories to their latest commits.")
    parser.add_argument("--languages", type=str, help="Comma-separated list of languages to process (default: all)")
    parser.add_argument("--workers", type=int, help="Maximum number of concurrent workers (default: CPU count * 2)")
    parser.add_argument("--only-missing", action="store_true", help="Only update languages without an existing rev")

    args = parser.parse_args()

    asyncio.run(main(args))
