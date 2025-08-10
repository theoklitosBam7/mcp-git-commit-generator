# MCP Git Commit Generator: AI Agent Guide

## Project Overview

This MCP server generates conventional commit messages from staged git changes. It exposes two main MCP tools:

- `generate_commit_message`: Analyzes staged changes and generates a commit message (type/scope can be auto-detected or provided)
- `check_git_status`: Reports staged, unstaged, and untracked files

## Architecture & Key Files

- `src/mcp_git_commit_generator/server.py`: Implements MCP tools with `@mcp.tool()` and all commit message logic
- `src/mcp_git_commit_generator/__init__.py`: CLI entrypoint using Click; always use `--option value` (never positional args)
- `src/mcp_git_commit_generator/__main__.py`: Simple module launcher
- `inspector/`: Inspector UI (Node.js, optional for debugging and tool testing)

Transport options:

- `stdio` (default, for CLI/MCP clients)
- `sse` (for Inspector UI/web clients)

## Developer Workflow

### Environment Setup

- Recommended: `uv venv`, `uv pip install -r pyproject.toml --group dev`, `uv pip install -e .`
- Or: `python -m venv .venv`, `pip install -e .`, `pip install -r requirements-dev.txt`

### Running & Debugging

- Start server: `mcp-git-commit-generator [--transport sse] [--host ...] [--port ...] [-v]`
- VS Code tasks:
  - **Start MCP Server**: Debug server on port 5678 (SSE transport)
  - **Start MCP Inspector**: Launches Inspector UI (depends on server)
- Inspector UI: `cd inspector && npm run dev:inspector` (Node.js required)

### Docker

- Build: `docker build -t mcp-git-commit-generator .`
- Run (default): `docker run -i --rm --mount type=bind,src=${HOME},dst=${HOME} mcp-git-commit-generator`
- Run (SSE): `docker run -d -p 3001:3001 --entrypoint mcp-git-commit-generator ... --transport sse --host 0.0.0.0 --port 3001`

## Project Conventions & Patterns

- CLI always uses `--option value` (never positional args)
- MCP tools are defined with `@mcp.tool()` and detailed docstrings in `server.py`
- Git repo validation via `get_valid_repo_path` helper
- Git commands use `subprocess.run` with error handling
- Inspector UI is optional for debugging and tool testing
- Versioning: update `pyproject.toml` for releases
- Docker image is published on tag pushes starting with "v"

## Integration Points & Client Configs

- MCP clients: VS Code, Cursor, Windsurf, Claude Desktop (see README for Docker config examples)
- Inspector UI: for interactive tool testing/debugging

## Quick Usage Example

1. Stage changes: `git add <files>`
2. Use `check_git_status` to review staged/unstaged files
3. Use `generate_commit_message` to create a conventional commit message
4. Commit with the generated message

## Advanced Configuration

- See README for `.vscode/mcp.json` and Docker usage details
- Inspector UI available at `http://localhost:5173` when running locally

## Key Patterns for AI Agents

- All commit message logic and new MCP tools should be added in `server.py`
- Always validate git repo paths before running git commands
- Use subprocess with error handling for all git operations
- Inspector UI is for tool testing/debugging, not required for normal operation

## Feedback & Issues

Open issues or suggestions on GitHub: https://github.com/theoklitosBam7/mcp-git-commit-generator/issues

## Examples

- To add a new MCP tool: define a function in `server.py` with `@mcp.tool()` and a docstring describing parameters/usage
- To debug: use VS Code tasks or Inspector UI; breakpoints work in MCP tool code

## Key Dependencies

- `mcp[cli]` (core MCP)
- `click` (CLI)
- `debugpy` (dev/debugging)
- Inspector UI: Node.js, `@modelcontextprotocol/inspector` (optional)
