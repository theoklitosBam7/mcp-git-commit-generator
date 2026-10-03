# AGENTS.md

Guidance for agents working in this repository.

## Build and test

- `uv sync --all-groups` installs the locked development environment.
- `uv run pytest` runs the test suite.
- `uv run python -m compileall -q src tests` checks Python syntax.
- `uv build` builds release artifacts from the lockfile.
- `uv run mcp-git-commit-generator --transport streamable-http` starts the HTTP development server at `127.0.0.1:3001/mcp`.
- `cd inspector && npm ci && npm run dev:inspector` starts MCP Inspector v2.

## MCP compatibility

- The server uses `MCPServer` from the official Python MCP SDK v2.
- The target protocol is `2026-07-28`; the SDK also serves legacy MCP clients.
- `stdio` is the default transport. Use Streamable HTTP for network serving.
- SSE remains only for legacy compatibility and must not be the default in new examples.
- Protocol tests must cover both modern `2026-07-28` and legacy client modes.

## Security and implementation requirements

- Git subprocesses must use `cwd=` and must never use `shell=True`.
- Use `_run_git()` so Git commands keep the timeout, non-interactive environment, no external diff, and pager controls.
- Treat repository content as untrusted model input. Do not interpolate raw repository text into instruction sections.
- Keep the staged diff preview capped at 1500 characters unless a deliberate design change is tested.
- Validate model-facing preference fields before adding them to generated prompts.
- Bind HTTP development servers to loopback by default. A non-loopback bind must be an explicit operator choice.
- Keep GitHub Actions pinned to full commit SHAs and retain the release tag in a same-line comment for update tooling.
- Keep Python and npm lockfiles current. Do not merge dependency changes with stale lockfiles.
- The container must run as a non-root user and should not gain Linux capabilities it does not need.
