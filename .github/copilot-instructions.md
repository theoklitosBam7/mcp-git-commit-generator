# MCP Git Commit Generator: AI Agent Guide

## Project Overview

This MCP server generates conventional commit messages from staged git changes. It exposes two main MCP tools:

- `generate_commit_message`: Analyzes staged changes and generates a conventional commit message. Commit type and scope can be auto-detected or provided.
- `check_git_status`: Reports staged, unstaged, and untracked files with clear validation of the git repository path.

## Architecture & Key Files

- **Server Logic**: All commit message logic and MCP tools are defined in `src/mcp_git_commit_generator/server.py` using the `@mcp.tool()` decorator. This includes helper functions like `get_valid_repo_path` and robust error handling with `subprocess.run` for git operations.
- **CLI Entrypoint**: The CLI is handled via `src/mcp_git_commit_generator/__init__.py`, which enforces using `--option value` for all command-line arguments.
- **Module Launcher**: Bootstrapping of the server is done through `src/mcp_git_commit_generator/__main__.py`.
- **Inspector UI**: Located in the `inspector/` directory, this Node.js-based tool aids in debugging and interactive testing of MCP tools (accessible via `npm run dev:inspector`).

## Developer Workflow & Commands

### Environment Setup

- Recommended: Create a virtual environment using `uv venv` then install development requirements with:
  - `uv pip install -r pyproject.toml --group dev`
  - `uv pip install -e .`
- Alternatively:
  - `python -m venv .venv`
  - `pip install -e . && pip install -r requirements-dev.txt`

### Running & Debugging

- **Start MCP Server**: Use the provided VS Code task "Start MCP Server" which runs the server with SSE transport on port 5678 (see `debugpy` configuration in `server.py`).
- **Start MCP Inspector**: Launch via the VS Code task "Start MCP Inspector". It requires the MCP Server to be running and is configured to use Node.js (refer to `inspector/package.json`).

### Docker Usage

- **Build**: `docker build -t mcp-git-commit-generator .`
- **Run**:
  - Default: `docker run -i --rm --mount type=bind,src=${HOME},dst=${HOME} mcp-git-commit-generator`
  - With SSE: `docker run -d -p 3001:3001 --entrypoint mcp-git-commit-generator ... --transport sse --host 0.0.0.0 --port 3001`

## Project-Specific Conventions & Patterns

- **Command Line Usage**: Always use `--option value`. Positional arguments are not supported.
- **MCP Tool Definitions**: New tools must be defined in `server.py` with detailed docstrings. Follow the convention used in existing tools like `generate_commit_message` and `check_git_status`.
- **Git Operations**: Always validate the git repo with `get_valid_repo_path`. Git commands are executed using `subprocess.run` with structured error handling.
- **Inspector UI & Debugging**: The Inspector UI (found in `inspector/`) is optional but useful for testing new tool integrations. It runs on `http://localhost:5173` when started.
- **Versioning & Releases**: Update `pyproject.toml` according to semver before releasing. Docker images are published on tag pushes starting with "v".

## Integration Points & Communication

- **MCP Clients**: Integrates with VS Code, Cursor, Windsurf, and Claude Desktop. Refer to the README and CI/CD configuration for detailed Docker and client setup examples.
- **Inter-Component Communication**: The server supports both `stdio` and `sse` transports. Ensure that any new integration or tool follows the patterns established in `server.py` and related CLI configuration.

## Example Usage

1. Stage changes: `git add <files>`
2. Run `check_git_status` to verify the current git state.
3. Generate a conventional commit message with `generate_commit_message`.
4. Commit using the generated message.

## Key Patterns for AI Agents

- **Focus on Key Files**: Read `server.py` for all MCP tool logic and refer to `__init__.py` for CLI conventions.
- **Agent Guidance**: When building new agent features, follow the example patterns in this guide. Use inline comments with `// ...existing code...` to contextualize changes (see developer instructions).
- **Collaboration & Feedback**: Always verify that new implementations integrate well with the established patterns for git operations, Docker usage, and the Inspector UI.

## Feedback & Iteration

Please review these updated instructions and provide feedback on any unclear or incomplete sections so that we can iterate further.
