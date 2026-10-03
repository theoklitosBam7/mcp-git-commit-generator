# MCP Git Commit Generator

[![PyPI](https://img.shields.io/pypi/v/mcp-git-commit-generator.svg)](https://pypi.org/project/mcp-git-commit-generator/)
[![GitHub Release](https://img.shields.io/github/v/release/theoklitosBam7/mcp-git-commit-generator)](https://github.com/theoklitosBam7/mcp-git-commit-generator/releases)
[![CI](https://github.com/theoklitosBam7/mcp-git-commit-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/theoklitosBam7/mcp-git-commit-generator/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/theoklitosBam7/mcp-git-commit-generator.svg)](https://github.com/theoklitosBam7/mcp-git-commit-generator/blob/main/LICENSE)

Generate Conventional Commit messages from staged Git changes through the Model Context Protocol (MCP).

## MCP compatibility

This release uses the official Python MCP SDK v2 and targets the **MCP 2026-07-28** specification.

The SDK can serve both protocol eras:

- Modern clients use the 2026-07-28 `server/discover` flow.
- Older clients can still use the legacy `initialize` handshake.
- `stdio` is the default local transport.
- `streamable-http` is the recommended network transport. Its default endpoint is `/mcp`.
- `sse` remains available only for legacy integrations.

This server configures Streamable HTTP as stateless JSON because its tools do not need a server-to-client back-channel.

## Features

- Generate a Conventional Commit prompt from staged changes only.
- Inspect staged, unstaged, and untracked files.
- Accept a repository root or a path inside a Git worktree.
- Cap the staged diff preview at 1500 characters.
- Treat repository text as untrusted model input.
- Validate `commit_type` and `scope` before they enter a model prompt.
- Run Git without a shell, external diff, pager, or interactive prompts.
- Apply a 15-second timeout to Git commands.
- Support stdio, Streamable HTTP, and legacy SSE.
- Run the published container as a non-root user.
- Test modern MCP 2026-07-28 and legacy MCP behavior.

## Requirements

- Python 3.14 or later.
- Git.
- An MCP-compatible client.
- Optional: Docker.
- Optional: Node.js 22.19 or later for MCP Inspector v2.

## Install

### uvx

```sh
uvx mcp-git-commit-generator
```

### PyPI

```sh
pip install mcp-git-commit-generator
```

### Docker

Mount only the repository that the server must inspect. A read-only mount is enough because the tools do not create commits or edit files.

```sh
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --mount type=bind,src="$PWD",dst="$PWD",readonly \
  ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest
```

## Tools

### `generate_commit_message`

Build a strict prompt for a Conventional Commit message from staged changes.

Parameters:

- `repo_path`: optional repository path. A path inside a worktree is accepted.
- `commit_type`: optional Conventional Commit type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `build`, `ci`, `test`, `chore`, or `revert`.
- `scope`: optional 1-50 character scope. It can contain letters, numbers, `.`, `_`, `/`, and `-`.

### `check_git_status`

Report the current branch plus staged, unstaged, and untracked files.

Parameter:

- `repo_path`: optional repository path. A path inside a worktree is accepted.

## Client configuration

### uvx with stdio

Common MCP client format:

```json
{
  "mcpServers": {
    "mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

VS Code uses a top-level `servers` object:

```json
{
  "servers": {
    "mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

### Streamable HTTP

Start the local server:

```sh
uv run mcp-git-commit-generator \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 3001
```

Connect the client to:

```text
http://127.0.0.1:3001/mcp
```

The HTTP mode has no application authentication. The default bind address is loopback for this reason. If you need remote access, put the server behind an authenticated TLS reverse proxy and restrict network access.

### Legacy SSE

Older clients can still use SSE:

```sh
uv run mcp-git-commit-generator \
  --transport sse \
  --host 127.0.0.1 \
  --port 3001
```

New integrations should use stdio or Streamable HTTP.

## Development

Install the locked environment:

```sh
uv sync --all-groups
```

Run the checks:

```sh
uv run python -m compileall -q src tests
uv run pytest
uv run pip-audit --local
uv build
```

### MCP Inspector v2

Start the MCP server in one terminal from the repository root:

```sh
uv run mcp-git-commit-generator \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 3001
```

In another terminal, start Inspector with the local server configured:

```sh
cd inspector
npm ci
npm run dev:inspector -- \
  --transport http \
  --server-url http://127.0.0.1:3001/mcp \
  --protocol-era modern
```

Open the Inspector URL printed in the terminal, normally at `http://127.0.0.1:6274`. If the local server's connection switch is off, turn it on. Inspector calls the transport `http`; the Python server calls it `streamable-http`.

The `/mcp` URL is a protocol endpoint, not a web interface. Do not open it directly in the browser to use Inspector.

For VS Code debugging, select the project's `.venv` Python interpreter, install the Inspector dependencies with `npm ci` in `inspector`, and run **Debug in Inspector (Chrome)** or **Debug in Inspector (Edge)**. These configurations start both processes and open Inspector on port `5173`.

## CI and supply-chain controls

The repository uses these controls:

- GitHub Actions are pinned to full commit SHAs.
- Python tests run on Linux, macOS, and Windows.
- Python dependencies are locked with `uv.lock` and audited with `pip-audit`.
- Inspector dependencies are locked with `package-lock.json` and checked with `npm audit`.
- Pull requests use GitHub dependency review for high-severity dependency changes.
- Dependabot checks uv, npm, GitHub Actions, and Docker dependencies.
- Container builds produce provenance and an SBOM.
- PyPI publishing uses GitHub OIDC trusted publishing and package attestations.

## Security model

Repository names, paths, file contents, and diffs are attacker-controlled input. The server serializes repository context as JSON and tells the downstream model to use those values only as evidence about the change. It does not treat instructions hidden inside a staged diff as trusted instructions.

Git is executed as an argument list with `shell=False` behavior. The server disables external diffs, interactive prompts, and pagers for tool operations. It also applies a command timeout.

For Docker, prefer a narrow read-only repository mount instead of mounting the whole home directory.

## Release

1. Update `version` in `pyproject.toml`.
2. Run all checks and refresh both lockfiles.
3. Create a matching tag, for example `v3.0.0`.
4. Push the tag.

Tag pushes build and publish the Python package and container image. PyPI uses trusted publishing.

## License

[MIT](./LICENSE) © 2025-2026 Theoklitos Bampouris
