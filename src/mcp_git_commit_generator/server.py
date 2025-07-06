"""
FastMCP Server for generating conventional commit messages from git diff
"""

import logging
import os
import subprocess
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Git Commit Generator")


def get_valid_repo_path(repo_path: Optional[str]) -> Optional[str]:
    """
    Resolve and validate the git repository path.
    Returns the valid repo path if valid, otherwise None.
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "[get_valid_repo_path] Using current working directory: %s",
        repo_path or os.getcwd(),
    )
    if repo_path is None:
        repo_path = os.getcwd()
    if not os.path.isdir(repo_path) or not os.path.exists(
        os.path.join(repo_path, ".git")
    ):
        return None
    return repo_path


@mcp.tool()
def generate_commit_message(
    repo_path: Optional[str] = None,
    commit_type: Optional[str] = None,
    scope: Optional[str] = None,
) -> str:
    """
    Generate a conventional commit message based on staged git changes.

    Args:
        repo_path: Optional path to the target git repository. If not provided, uses the current working directory.
        commit_type: Optional commit type (feat, fix, docs, style, refactor, perf, build, ci, test, chore, revert)
        scope: Optional scope of the change

    Returns:
        Analysis of git changes for generating conventional commit messages
    """
    try:
        valid_repo_path = get_valid_repo_path(repo_path)
        if not valid_repo_path:
            return f"Path '{repo_path or os.getcwd()}' is not a valid git repository."
        cwd = valid_repo_path
        # Get staged changes
        diff_result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )

        if not diff_result.stdout.strip():
            return "No staged changes found. Please stage your changes with 'git add' first."

        # Get git status for context
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )

        # Get list of changed files for better analysis
        files_result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )

        # Prepare analysis for the AI
        analysis = f"""
            ## Git Change Analysis for Conventional Commit Message

            ### Changed Files:
            {files_result.stdout}

            ### File Status Summary:
            {status_result.stdout}

            ### Diff Preview (first 1500 chars):
            {diff_result.stdout[:1500]}

            ### User Preferences:
            - Requested commit type: {commit_type or "auto-detect based on changes"}
            - Requested scope: {scope or "auto-detect based on files changed"}

            ### Instructions:
            Please generate a conventional commit message following this format:
            `type(scope): description`

            **Common types:**
            - feat: A new feature
            - fix: A bug fix
            - docs: Documentation only changes
            - style: Changes that don't affect meaning (white-space, formatting, etc)
            - refactor: Code change that neither fixes a bug nor adds a feature
            - perf: A code change that improves performance
            - build: Changes that affect the build system or external dependencies
            - ci: Changes to our CI configuration files and scripts
            - test: Adding missing tests or correcting existing tests
            - chore: Changes to build process or auxiliary tools
            - revert: Reverts a previous commit

            **Guidelines:**
            - Use imperative mood in description ("add" not "adds" or "added")
            - Don't capitalize first letter of description
            - No period at the end of description
            - Keep description under 50 characters if possible
            - If scope is obvious from files, include it in parentheses
            - If too many files are changed, consider summarizing the changes using list format in the commit body
            - In the commit body list, use imperative mood, capitalize the first letter, and do not use a period at the end
            """

        return analysis

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or str(e)
        return f"Git command failed: {error_msg}"
    except FileNotFoundError:
        return "Git is not installed or not found in PATH"
    except Exception as e:
        return f"Error analyzing git changes: {str(e)}"


def _parse_git_status_line(line):
    """
    Helper to parse a single git status line.
    Returns (staged_file, unstaged_file, untracked_file)
    """
    if len(line) < 2:
        return None, None, None
    staged_status = line[0]
    unstaged_status = line[1]
    filename = line[3:]
    if staged_status == "?" and unstaged_status == "?":
        return None, None, filename
    staged_file = f"{staged_status} {filename}" if staged_status != " " else None
    unstaged_file = f"{unstaged_status} {filename}" if unstaged_status != " " else None
    return staged_file, unstaged_file, None


def _parse_git_status_lines(status_lines):
    staged_files = []
    unstaged_files = []
    untracked_files = []
    for line in status_lines:
        staged_file, unstaged_file, untracked_file = _parse_git_status_line(line)
        if staged_file:
            staged_files.append(staged_file)
        if unstaged_file:
            unstaged_files.append(unstaged_file)
        if untracked_file:
            untracked_files.append(untracked_file)
    return staged_files, unstaged_files, untracked_files


@mcp.tool()
def check_git_status(repo_path: Optional[str] = None) -> str:
    """
    Check the current git repository status.

    Args:
        repo_path: Optional path to the target git repository. If not provided, uses the current working directory.

    Returns:
        Current git status including staged, unstaged, and untracked files
    """
    try:
        valid_repo_path = get_valid_repo_path(repo_path)
        if not valid_repo_path:
            return f"Path '{repo_path or os.getcwd()}' is not a valid git repository."
        cwd = valid_repo_path
        # Get full git status
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )

        # Get branch info
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )

        current_branch = branch_result.stdout.strip()

        if not status_result.stdout.strip():
            return f"Repository is clean on branch '{current_branch}'. No changes to commit."

        # Parse status using helper
        status_lines = status_result.stdout.strip().split("\n")
        staged_files, unstaged_files, untracked_files = _parse_git_status_lines(
            status_lines
        )

        status_summary = f"Current branch: {current_branch}\n\n"

        if staged_files:
            status_summary += "Staged files (ready to commit):\n"
            status_summary += "\n".join(f"  {file}" for file in staged_files)
            status_summary += "\n\n"

        if unstaged_files:
            status_summary += "Unstaged files (need to be added):\n"
            status_summary += "\n".join(f"  {file}" for file in unstaged_files)
            status_summary += "\n\n"

        if untracked_files:
            status_summary += "Untracked files:\n"
            status_summary += "\n".join(f"  {file}" for file in untracked_files)
            status_summary += "\n\n"

        if staged_files:
            status_summary += "✓ Ready to generate commit message!"
        else:
            status_summary += (
                "ℹ Stage some files with 'git add' to generate commit messages."
            )

        return status_summary

    except subprocess.CalledProcessError as e:
        return f"Git command failed: {e.stderr or e.stdout or str(e)}"
    except FileNotFoundError:
        return "Git is not installed or not found in PATH"
    except Exception as e:
        return f"Error checking git status: {str(e)}"


if __name__ == "__main__":
    mcp.run()
