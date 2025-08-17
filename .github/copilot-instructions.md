# MCP Git Commit Generator: AI Agent Guide

## Project Overview

This MCP server generates conventional commit messages from staged git changes. It exposes two main MCP tools:

- `generate_commit_message`: Analyzes staged changes and generates a conventional commit message. Commit type and scope can be auto-detected or provided.
- `check_git_status`: Reports staged, unstaged, and untracked files with clear validation of the git repository path.

## Architecture & Key Files

- **MCP Tool Logic**: All tool logic is in `src/mcp_git_commit_generator/server.py` using the `@mcp.tool()` decorator. Helper functions like `_get_valid_repo_path` and robust error handling with `subprocess.run` are standard.
- **CLI Entrypoint**: `src/mcp_git_commit_generator/__init__.py` enforces strict `--option value` usage for all CLI arguments (never use positional args).
- **Module Launcher**: `src/mcp_git_commit_generator/__main__.py` bootstraps the server for `python -m` and CLI use.
- **Inspector UI**: The `inspector/` directory contains a Node.js-based tool for interactive MCP tool testing (`npm run dev:inspector`).

## Developer Workflow & Commands

### Environment Setup

- **Recommended**: `uv venv` → `uv pip install -r pyproject.toml --group dev` → `uv pip install -e .`
- **Alternative**: `python -m venv .venv` → `pip install -e . && pip install -r requirements-dev.txt`

### Running & Debugging

- **VS Code Tasks**: Use "Start MCP Server" (SSE, port 5678) and "Start MCP Inspector" for local development. Inspector UI runs at `http://localhost:5173`.
- **Local CLI**: Run with `mcp-git-commit-generator --transport sse` or `python -m mcp_git_commit_generator --transport sse` (always use `--option value`).
- **Docker**: Build with `docker build -t mcp-git-commit-generator .`. Run with:
  - Default: `docker run -i --rm --mount type=bind,src=${HOME},dst=${HOME} mcp-git-commit-generator`
  - SSE: `docker run -d -p 3001:3001 --entrypoint mcp-git-commit-generator ... --transport sse --host 0.0.0.0 --port 3001`

### Inspector UI Workflow

1. Start the server (see above)
2. From `inspector/`, run `npm run dev:inspector`
3. Open `http://localhost:5173` and connect to the running MCP server
4. Use the UI to list, invoke, and debug tools interactively

## Project-Specific Conventions & Patterns

- **CLI Usage**: Always use `--option value` for all arguments. Positional arguments are not supported and will error.
- **MCP Tool Definitions**: Define new tools in `server.py` with detailed docstrings and robust error handling. Follow the pattern of `generate_commit_message` and `check_git_status`.
- **Git Operations**: Always validate the repo path with `_get_valid_repo_path`. Use `subprocess.run` for all git commands, with structured error handling.
- **Testing**: Run tests with `pytest`, e.g. `pytest -v` or `pytest --cov=src/mcp_git_commit_generator`.
- **Versioning**: Update `pyproject.toml` for releases. Docker images are published on tag pushes starting with "v".

## Integration Points & Communication

- **MCP Clients**: Integrates with VS Code, Cursor, Windsurf, and Claude Desktop. See README for config examples.
- **Transports**: Supports both `stdio` and `sse` (for Inspector UI and remote access). Match your client config to the server mode.

## Example Usage

1. Stage changes: `git add <files>`
2. Run `check_git_status` to verify the current git state
3. Generate a commit message with `generate_commit_message`
4. Commit using the generated message

## Key Patterns for AI Agents

- **Focus on Key Files**: Use `server.py` for tool logic, `__init__.py` for CLI conventions
- **Agent Guidance**: When building new features, follow the code and docstring patterns in this guide. Use inline comments like `// ...existing code...` to contextualize changes
- **Integration**: Ensure new code fits the established patterns for git ops, Docker, and Inspector UI

## Feedback & Iteration

Please review these instructions and provide feedback on any unclear or incomplete sections so they can be improved.
