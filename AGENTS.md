# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Build/Test Commands

- `uv run pytest` - Run all tests (uses pytest with pythonpath=src)
- `uv run pytest tests/test_server.py` - Run specific test file
- `uv run pytest -v` - Run tests with verbose output
- `uv run pytest --cov=src/mcp_git_commit_generator` - Run tests with coverage
- `uv sync --group dev` - Install dependencies with dev tools
- `uv run mcp-git-commit-generator --transport sse` - Run server with SSE transport (required for Inspector UI)
- `cd inspector && npm install && npm run dev:inspector` - Start Inspector UI (requires SSE server running on port 3001)

## Critical Implementation Details

- Git commands MUST use `cwd=cwd` parameter in subprocess.run() to target the correct repository
- Path resolution uses `os.path.realpath(os.path.expanduser())` to handle tilde and symlinks
- Diff preview is truncated to 1500 characters in generate_commit_message for analysis
- Inspector UI requires SSE transport (stdio won't work) - server runs on port 3001, inspector on port 5173
- pytest config has `pythonpath = ["src"]` - critical for imports to work in tests
- Build backend is `uv_build` (not standard setuptools) - requires `uv` for building
- Tests need git config setup in CI: `git config --global user.email "ci@example.com" && git config --global user.name "CI Runner"`
- Server uses FastMCP framework from `mcp.server.fastmcp` - tools decorated with `@mcp.tool()`
- LOG_LEVEL env var overrides logging (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- Two MCP tools: `generate_commit_message` (analyzes staged changes) and `check_git_status` (reports repo state)
