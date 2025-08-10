# MCP Git Commit Generator 🚀

Generate conventional commit messages from your staged git changes using Model Context Protocol (MCP).

## ✨ Features

- **Automatic commit message generation** based on staged git diffs.
- Supports [Conventional Commits](https://www.conventionalcommits.org/).
- MCP server with both stdio (default) and SSE transport options.
- Inspector UI for interactive inspection (via MCP Inspector).

## 📦 Requirements

- **For Docker usage**: [Docker](https://www.docker.com/) (for running the server in a container)
- **For PyPI/uvx usage**: [Python](https://www.python.org/) >= 3.13.5 and [uv](https://github.com/astral-sh/uv)
  (recommended) or pip
- [Git](https://git-scm.com/) (for version control)
- An MCP-compatible client (VS Code with MCP extension, Claude Desktop, Cursor, Windsurf, etc.)

## 🚀 Installation

You can install and use the MCP Git Commit Generator in multiple ways:

### Option 1: Using uvx (Recommended)

The easiest way to use the package is with `uvx`, which automatically manages the virtual environment:

```sh
uvx mcp-git-commit-generator
```

### Option 2: Install from PyPI

```sh
pip install mcp-git-commit-generator
```

Or with uv:

```sh
uv pip install mcp-git-commit-generator
```

### Option 3: Using Docker

Use the pre-built Docker image from GitHub Container Registry (no installation required):

```sh
docker run -i --rm --mount type=bind,src=${HOME},dst=${HOME} ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest
```

## 🛠️ Available Tools

This MCP server provides the following tools to help you generate conventional commit messages:

### `generate_commit_message`

Generates a conventional commit message based on your staged git changes.

**Parameters:**

- `repo_path` (string, optional): Path to the git repository. If omitted, uses the current directory.
- `commit_type` (string, optional): Conventional commit type (e.g., `feat`, `fix`, `docs`, `style`, `refactor`,
  `perf`, `build`, `ci`, `test`, `chore`, `revert`). If omitted, the type will be auto-detected.
- `scope` (string, optional): Scope of the change (e.g., file or module name). If omitted, the scope will be
  auto-detected based on changed files.

**Usage:**

1. Stage your changes: `git add <files>`
2. Use the tool through your MCP client to generate a commit message
3. The tool will analyze your staged changes and generate an appropriate conventional commit message

### `check_git_status`

Checks the current git repository status, including staged, unstaged, and untracked files.

**Parameters:**

- `repo_path` (string, optional): Path to the git repository. If omitted, uses the current directory.

**Usage:**

Use this tool to get an overview of your current git repository state before generating commit messages.

## 🧩 MCP Client Configuration

Configure the MCP Git Commit Generator in your favorite MCP client. You have multiple options:

1. **Using uvx** (recommended - automatically manages dependencies)
2. **Using Docker** (no local Python installation required)
3. **Using local Python installation** (for development)

### VS Code

Add one of the following configurations to your VS Code `mcp.json` file (usually located at `.vscode/mcp.json` in your workspace):

#### Using uvx (Recommended)

```jsonc
{
  "servers": {
    "mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

#### Using Docker

```jsonc
{
  "servers": {
    "mcp-git-commit-generator": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=${userHome},dst=${userHome}",
        "ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest"
      ]
    }
  }
}
```

If you want to put the configuration in your user `settings.json` file, you can do so by adding:

```jsonc
{
  "mcp": {
    "servers": {
      "mcp-git-commit-generator": {
        "command": "uvx",
        "args": ["mcp-git-commit-generator"]
      }
    }
  }
}
```

### Cursor

Add one of the following to your Cursor MCP configuration file (usually located at `~/.cursor/mcp.json`):

#### Cursor with uvx (Recommended)

```jsonc
{
  "mcpServers": {
    "mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

#### Cursor with Docker

```jsonc
{
  "mcpServers": {
    "mcp-git-commit-generator": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=${userHome},dst=${userHome}",
        "ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest"
      ]
    }
  }
}
```

### Windsurf

Configure Windsurf with one of the following MCP server settings (usually located at `~/.codeium/windsurf/mcp_config.json`):

#### Windsurf with uvx (Recommended)

```jsonc
{
    "mcpServers": {
      "mcp-git-commit-generator": {
        "command": "uvx",
        "args": ["mcp-git-commit-generator"]
      }
    }
}
```

#### Windsurf with Docker

```jsonc
{
    "mcpServers": {
      "mcp-git-commit-generator": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "--mount",
          "type=bind,src=${userHome},dst=${userHome}",
          "ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest"
        ]
      }
    }
}
```

### Claude Desktop

Add one of the following to your Claude Desktop configuration file (usually located at
`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

#### Claude Desktop with uvx (Recommended)

```jsonc
{
  "mcpServers": {
    "mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

#### Claude Desktop with Docker

```jsonc
{
  "mcpServers": {
    "mcp-git-commit-generator": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=${userHome},dst=${userHome}",
        "ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest"
      ]
    }
  }
}
```

> **Note**: The `--mount` option in Docker configurations allows the Docker container to access your home
> directory, enabling it to work with git repositories located anywhere in your file system. When using uvx or pip
> installations, this mounting is not needed as the tool runs directly on your system. Adjust the mount path if your
> repositories are located elsewhere when using Docker.

## 🚀 Quick Start Guide

1. **Install the package** using one of the methods above:
   - **Recommended**: `uvx mcp-git-commit-generator` (or configure in your MCP client)
   - **Alternative**: `pip install mcp-git-commit-generator`
   - **Docker**: Use the configurations above with Docker
2. **Configure your MCP client** using one of the configurations above
3. **Stage some changes** in a git repository:

   ```sh
   git add <files>
   ```

4. **Use the tools** through your MCP client:
   - Use `check_git_status` to see your current repository state
   - Use `generate_commit_message` to create a conventional commit message
5. **Commit your changes** with the generated message

---

## 👨‍💻 Developer Guidelines

The following sections are intended for developers who want to contribute to or modify the MCP Git Commit Generator.

### Local Development Setup 🛠️

If you prefer not to use Docker for development, you can run the server locally:

**Requirements:**

- [Python](https://www.python.org/) >= 3.13.5
- [MCP CLI](https://pypi.org/project/mcp/) >= 1.10.1
- [uv](https://github.com/astral-sh/uv) (for dependency management, optional but recommended)
- [Node.js](https://nodejs.org/en) (for Inspector UI, optional)
- [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) (for debugging, optional)

**Installation:**

1. **Clone the repository:**

   ```sh
   git clone https://github.com/theoklitosBam7/mcp-git-commit-generator.git
   cd mcp-git-commit-generator
   ```

2. **Prepare environment:**

    There are two approaches to set up the environment for this project. You can choose either one based on your preference.

    > Note: Reload VSCode or terminal to ensure the virtual environment python is used after creating the virtual environment.

    | Approach | Steps |
    | -------- | ----- |
    | Using `uv` | 1. Create virtual environment: `uv venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment <br>3. Install dependencies (include dev dependencies): `uv pip install -r pyproject.toml --group dev` <br>4. Install `mcp-git-commit-generator` using the command: `uv pip install -e .`. |
    | Using `pip` | 1. Create virtual environment: `python -m venv .venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment <br>3. Install dependencies: `pip install -e .`. <br>4. Install pip dev dependencies: `pip install -r requirements-dev.txt`. |

3. **(Optional) Install Inspector dependencies:**

   ```sh
   cd inspector
   npm install
   ```

### 📦 Publishing to PyPI

The project includes an automated PyPI publishing workflow (`.github/workflows/pypi-publish.yml`) that:

- **Triggers on**: Tag pushes matching `v*.*.*` pattern, manual workflow dispatch, or pull requests to main
- **Builds**: Python package distributions using the `build` package
- **Publishes**: Automatically publishes to PyPI using trusted publishing (OIDC) when tags are pushed

To publish a new version:

1. Update the version in `pyproject.toml`
2. Create and push a git tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
3. The workflow will automatically build and publish to PyPI

### 🐳 Building and Running with Docker

You can build and run the MCP Git Commit Generator using Docker. The provided Dockerfile uses a multi-stage build
with [`uv`](https://github.com/astral-sh/uv) for dependency management and runs the server as a non-root user for security.

#### Build the Docker image

```sh
docker build -t mcp-git-commit-generator .
```

#### Run the server in a container (default: stdio transport)

You can run the published image directly from GitHub Container Registry.

```sh
docker run -d \
  --name mcp-git-commit-generator \
  ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest
```

By default, the container runs:

```sh
mcp-git-commit-generator --transport stdio
```

If you want to use SSE transport (for Inspector UI or remote access), override the entrypoint or run manually:

```sh
docker run -d \
  --name mcp-git-commit-generator \
  -p 3001:3001 \
  --entrypoint mcp-git-commit-generator \
  ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest --transport sse --host 0.0.0.0 --port 3001
```

The server will be available at `http://localhost:3001` when using SSE.

### 🖥️ Running the Server Locally

**To run locally (without Docker):**

1. Set up your uv or Python environment as described in the Local Development Setup section.
2. From the project root, run:

  <details>
  <summary>mcp-git-commit-generator</summary>

   ```sh
   # If you have mcp-git-commit-generator installed in your environment (default: stdio)
   mcp-git-commit-generator
   ```

  </details>

  <details>
  <summary>mcp-git-commit-generator with SSE transport</summary>

   ```sh
   mcp-git-commit-generator --transport sse
   ```

  </details>

  <details>
  <summary>Using uv</summary>

   ```sh
   uv run -m mcp_git_commit_generator --transport sse
   ```

  </details>

  <details>
  <summary>Using Python directly</summary>

   ```sh
   python -m mcp_git_commit_generator --transport sse
   ```

  </details>

  <br/>

  You can specify other options, for example:

   ```sh
   python -m mcp_git_commit_generator --transport sse --host 0.0.0.0 --port 3001 -v
   ```

   > The server listens on `0.0.0.0:3001` by default when using SSE, or as specified by the options above.

**Note:**

- If you want to use the CLI entrypoint, ensure the package is installed and your environment is activated.
- Do not use positional arguments (e.g., `python -m mcp_git_commit_generator sse`);
always use options like `--transport sse`.
- Available arguments with their values are:
  - `--transport`: Transport type (e.g., `stdio` (default), `sse`).
  - `--host`: Host to bind the server (default: `0.0.0.0`).
  - `--port`: Port to bind the server (default: `3001`).
  - `-v`, `--verbose`: Verbosity level (e.g., `-v`, `-vv`).

### 🔎 Start the Inspector UI

From the `inspector` directory:

```sh
npm run dev:inspector
```

> The Inspector UI will be available at `http://localhost:5173`.

### 🗂️ Project Structure

```sh
.
├── .github/                # GitHub workflows and issue templates
├── .gitignore
├── .markdownlint.jsonc
├── .python-version
├── .vscode/                # VSCode configuration
├── LICENSE
├── README.md
├── pyproject.toml          # Python project configuration
├── requirements-dev.txt    # Development dependencies
├── uv.lock                 # Python dependencies lock file
├── Dockerfile              # Docker build file
├── build/                  # Build artifacts
├── src/                    # Python source code
│   └── mcp_git_commit_generator/
│       ├── __init__.py     # Main entry point
│       ├── __main__.py     # CLI entry point
│       └── server.py       # Main server implementation
└── inspector/              # Inspector related files
    ├── package.json        # Node.js dependencies
    └── package-lock.json
```

### ⚙️ Advanced MCP Server Configuration for Development

The `.vscode/mcp.json` file configures how VS Code and related tools connect to your MCP Git Commit Generator server.
This file defines available server transports and their connection details, making it easy to switch between
different modes (stdio is default, SSE is optional) for development and debugging.

#### Example Development `mcp.json`

```jsonc
{
  "servers": {
    "mcp-git-commit-generator": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=${userHome},dst=${userHome}",
        "ghcr.io/theoklitosbam7/mcp-git-commit-generator:latest"
      ]
    },
    "sse-mcp-git-commit-generator": {
      "type": "sse",
      "url": "http://localhost:3001/sse"
    },
    "stdio-mcp-git-commit-generator": {
      "type": "stdio",
      "command": "${command:python.interpreterPath}",
      "args": ["-m", "mcp_git_commit_generator", "--transport", "stdio"]
    },
    "uvx-mcp-git-commit-generator": {
      "command": "uvx",
      "args": ["mcp-git-commit-generator"]
    }
  }
}
```

- **mcp-git-commit-generator**: Runs the server in a Docker container (default: stdio transport), using the published image.
- **sse-mcp-git-commit-generator**: Connects to the MCP server using Server-Sent Events (SSE) at `http://localhost:3001/sse`.
Only useful if you run the server with `--transport sse`.
- **stdio-mcp-git-commit-generator**: Connects using standard input/output (stdio), running the server as a subprocess.
This is the default and recommended for local development and debugging.
- **uvx-mcp-git-commit-generator**: Uses uvx to automatically install and run the package from PyPI.

### 🐞 Debugging the MCP Server

> Notes:
>
> - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a visual developer tool for testing
and debugging MCP servers.
> - All debugging modes support breakpoints, so you can add breakpoints to the tool implementation code.
> - **You can test tool arguments directly in the Inspector UI**: When using the Inspector, select a tool and provide
arguments in the input fields to simulate real usage and debug argument handling.

| Debug Mode | Description | Steps to debug |
| ---------- | ----------- | --------------- |
| MCP Inspector | Debug the MCP server using the MCP Inspector. | 1. Install [Node.js](https://nodejs.org/)<br> 2. Set up Inspector: `cd inspector` && `npm install` <br> 3. Open VS Code Debug panel. Select `Debug in Inspector (Edge)` or `Debug in Inspector (Chrome)`. Press F5 to start debugging.<br> 4. When MCP Inspector launches in the browser, click the `Connect` button to connect this MCP server.<br> 5. Then you can `List Tools`, select a tool, input parameters (see arguments above), and `Run Tool` to debug your server code.<br> |

### ⚙️ Default Ports and Customizations

| Debug Mode | Ports | Definitions | Customizations | Note |
| ---------- | ----- | ------------ | -------------- |-------------- |
| MCP Inspector | 3001 (Server, SSE only); 5173 and 3000 (Inspector) | [tasks.json](.vscode/tasks.json) | Edit [launch.json](.vscode/launch.json), [tasks.json](.vscode/tasks.json), [\_\_init\_\_.py](src/__init__.py), [mcp.json](.vscode/mcp.json) to change above ports.| N/A |

## 💬 Feedback

If you have any feedback or suggestions, please open an issue on the [MCP Git Commit Generator GitHub repository](https://github.com/theoklitosBam7/mcp-git-commit-generator/issues)

## 📄 License

[MIT](./LICENSE) License © 2025 [Theoklitos Bampouris](https://github.com/theoklitosBam7)
