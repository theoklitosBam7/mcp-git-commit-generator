"""
FastMCP Server for generating conventional commit messages from git diff
"""

import logging
import os
import subprocess
import textwrap
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("Git Commit Generator")


def _get_valid_repo_path(repo_path: Optional[str]) -> Optional[str]:
    """
    Resolve and validate the git repository path.
    Returns the valid repo path if valid, otherwise None.
    """
    logger = logging.getLogger(__name__)
    # Resolve user tilde and symlinks to a canonical path
    resolved = (
        os.path.realpath(os.path.expanduser(repo_path)) if repo_path else os.getcwd()
    )
    logger.info("[get_valid_repo_path] Resolved repository path: %s", resolved)
    if not os.path.isdir(resolved) or not os.path.exists(
        os.path.join(resolved, ".git")
    ):
        return None
    return resolved


@mcp.tool()
def generate_commit_message(
    repo_path: Optional[str] = None,
    commit_type: Optional[str] = None,
    scope: Optional[str] = None,
) -> str:
    """
    Prepare a structured analysis and instruction block for generating a
    Conventional Commit message from staged git changes only.

    Behavior:
        - Validates the repository path and operates on the provided repo or CWD.
        - Collects staged diff, porcelain status, and a name-status summary.
        - Incorporates optional user preferences for commit_type and scope.
        - Returns a single formatted string that includes context plus strict
          output instructions for an LLM to produce a Conventional Commit.

    Args:
        repo_path: Optional path to the target git repository. If not provided, uses the current working directory.
        commit_type: Optional commit type (feat, fix, docs, style, refactor, perf, build, ci, test, chore, revert)
        scope: Optional scope of the change

    Returns:
        A formatted prompt containing git change context and clear output rules
        for generating a Conventional Commit message
    """
    try:
        valid_repo_path = _get_valid_repo_path(repo_path)
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

        diff_preview = diff_result.stdout[:1500]
        analysis = textwrap.dedent(f"""
        ## Git Change Analysis for Conventional Commit Message

        ### Changed Files:
        {files_result.stdout}

        ### File Status Summary:
        {status_result.stdout}

        ### Diff Preview (first 1500 chars):
        {diff_preview}

        ### User Preferences:
            - Requested commit type: {commit_type or "auto-detect based on changes"}
            - Requested scope: {scope or "auto-detect based on files changed"}

        ### Task
        Write a Conventional Commit message for the STAGED changes only.

        ### Output format (return ONLY this)
        First line: type(scope): subject
        Add blank line before body
        Body paragraphs, each line <= 72 chars; bullets in body starting with "- "
        Optional footers (each on its own line), e.g.:
        BREAKING CHANGE: description

        ### Example generated commit message
        feat(core): add new feature

        - Implement new feature in core module
        - Update documentation

        BREAKING CHANGE: this change removes the old API method

        ### Rules
        - If commit_type or scope is provided above, USE THEM as-is.
        - If not provided, infer an appropriate type and a concise scope (or omit scope if unclear).
        - Subject: use imperative mood, start lowercase, no trailing period, <= 50 chars.
        - Body: use imperative mood (e.g. Update, Add etc.); explain WHAT and WHY, wrap at 72 chars; omit if subject suffices.
        - Use domain-specific terms; avoid generic phrases.
        - Do NOT mention "staged", "diff", or counts of files/lines.
        - Do NOT include markdown headers, code fences, or extra commentary.
        - Prefer a broad scope if many files; derive scope from top-level dirs when clear.
        - If there is a breaking change (e.g., API removal/rename), add a BREAKING CHANGE footer.
        - Keep the response to ONLY the commit message in the format above.

        ### Common types
        feat, fix, docs, style, refactor, perf, build, ci, test, chore, revert
        """)

        return analysis.strip()

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr or e.stdout or str(e)
        return f"Git command failed: {error_msg}"
    except FileNotFoundError:
        return "Git is not installed or not found in PATH"
    except OSError as e:
        return f"OS error occurred: {str(e)}"


def _parse_git_status_line(line):
    """
    Helper to parse a single git status line.
    Returns (staged_file, unstaged_file, untracked_file)
    """
    if len(line) < 3:
        return None, None, None
    staged_status = line[0]
    unstaged_status = line[1]
    filename = line[3:]
    if staged_status == "?" and unstaged_status == "?":
        return None, None, filename
    staged_file = filename if staged_status != " " else None
    unstaged_file = filename if unstaged_status != " " else None
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
        valid_repo_path = _get_valid_repo_path(repo_path)
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
        status_lines = [line for line in status_result.stdout.split("\n") if line]
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
        error_msg = e.stderr or e.stdout or str(e)
        return f"Git command failed: {error_msg}"
    except FileNotFoundError:
        return "Git is not installed or not found in PATH"
    except OSError as e:
        return f"OS error occurred: {str(e)}"


if __name__ == "__main__":
    mcp.run()
