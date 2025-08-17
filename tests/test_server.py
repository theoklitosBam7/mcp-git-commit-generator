"""
Unit tests for the MCP Git Commit Generator server tools.
"""

import subprocess

from mcp_git_commit_generator import server


def test_generate_commit_message_invalid_repo():
    """Test that an invalid repo path returns an error message."""
    result = server.generate_commit_message(repo_path="/not/a/repo")
    assert "not a valid git repository" in result


def test_check_git_status_invalid_repo():
    """Test that an invalid repo path returns an error message for git status."""
    result = server.check_git_status(repo_path="/not/a/repo")
    assert "not a valid git repository" in result


def test_generate_commit_message_no_staged_changes(tmp_path):
    """Test that no staged changes returns the appropriate message."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    result = server.generate_commit_message(repo_path=str(repo_dir))
    assert "No staged changes found" in result


def test_check_git_status_clean_repo(tmp_path):
    """Test that a clean repo returns the correct status message."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    result = server.check_git_status(repo_path=str(repo_dir))
    assert "No changes to commit" in result


def test_generate_commit_message_with_staged_change(tmp_path):
    """Test that a staged file produces a commit message analysis."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "foo.txt"
    file_path.write_text("hello world\n")
    subprocess.run(["git", "add", "foo.txt"], cwd=repo_dir, check=True)
    result = server.generate_commit_message(repo_path=str(repo_dir))
    assert "Git Change Analysis for Conventional Commit Message" in result
    assert "foo.txt" in result


def test_check_git_status_with_staged_and_unstaged(tmp_path):
    """Test that both staged and unstaged changes are reported correctly."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "bar.txt"
    file_path.write_text("first\n")
    subprocess.run(["git", "add", "bar.txt"], cwd=repo_dir, check=True)
    file_path.write_text("second\n")
    result = server.check_git_status(repo_path=str(repo_dir))
    assert "Staged files" in result
    assert "Unstaged files" in result
    assert "bar.txt" in result


def test_check_git_status_with_untracked_files(tmp_path):
    """Test that untracked files are reported correctly."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "untracked.txt"
    file_path.write_text("untracked\n")
    result = server.check_git_status(repo_path=str(repo_dir))
    assert "Untracked files" in result
    assert "untracked.txt" in result


def test_generate_commit_message_multiple_files_staged(tmp_path):
    """Test commit message analysis with multiple files staged."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file1 = repo_dir / "a.txt"
    file2 = repo_dir / "b.txt"
    file1.write_text("A\n")
    file2.write_text("B\n")
    subprocess.run(["git", "add", "a.txt", "b.txt"], cwd=repo_dir, check=True)
    result = server.generate_commit_message(repo_path=str(repo_dir))
    assert "a.txt" in result and "b.txt" in result


def test_check_git_status_with_staged_deletion(tmp_path):
    """Test that staged file deletions are reported correctly."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "delete_me.txt"
    file_path.write_text("bye\n")
    subprocess.run(["git", "add", "delete_me.txt"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "add file"], cwd=repo_dir, check=True)
    subprocess.run(["git", "rm", "delete_me.txt"], cwd=repo_dir, check=True)
    result = server.check_git_status(repo_path=str(repo_dir))
    print(result)
    assert "delete_me.txt" in result
    assert "Staged files" in result


def test_generate_commit_message_with_type_and_scope(tmp_path):
    """Test generate_commit_message with explicit commit_type and scope."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "scoped.txt"
    file_path.write_text("scoped\n")
    subprocess.run(["git", "add", "scoped.txt"], cwd=repo_dir, check=True)
    result = server.generate_commit_message(
        repo_path=str(repo_dir), commit_type="feat", scope="core"
    )
    assert "Requested commit type: feat" in result
    assert "Requested scope: core" in result


def test_generate_commit_message_breaking_change_prompt(tmp_path):
    """Test that the breaking change footer instructions are present in the prompt."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    file_path = repo_dir / "breaking.txt"
    file_path.write_text("breaking change\n")
    subprocess.run(["git", "add", "breaking.txt"], cwd=repo_dir, check=True)
    result = server.generate_commit_message(repo_path=str(repo_dir))
    assert "BREAKING CHANGE" in result
