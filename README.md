# MCP Git Commit Generator 🚀

Generate conventional commit messages from your staged git changes using Model Context Protocol (MCP).

## Features ✨

- **Automatic commit message generation** based on staged git diffs.
- Supports [Conventional Commits](https://www.conventionalcommits.org/).
- MCP server with both SSE and stdio transport options.
- Inspector UI for interactive inspection (via MCP Inspector).

## Requirements 📦

- [Docker](https://www.docker.com/) (for running the server in a container)
- [Git](https://git-scm.com/) (for version control)

If you prefer not to use Docker, you can run the server locally without it.

- [Python](https://www.python.org/) >= 3.13.5
- [MCP CLI](https://pypi.org/project/mcp/) >= 1.10.1
- [uv](https://github.com/astral-sh/uv) (for dependency management, optional but recommended)
- [Node.js](https://nodejs.org/en) (for Inspector UI, optional)
- [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) (for debugging, optional)

## Installation 🛠️

1. **Clone the repository:**

   ```sh
   git clone https://github.com/theoklitosBam7/mcp-git-commit-generator.git
   cd mcp-git-commit-generator
   ```

2. **Prepare environment (without Docker)**

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

---

## Run with Docker 🐳

You can build and run the MCP Git Commit Generator using Docker. The provided Dockerfile uses a multi-stage build
with [`uv`](https://github.com/astral-sh/uv)
for dependency management and runs the server as a non-root user for security.

### Build the Docker image

```sh
docker build -t mcp-git-commit-generator .
```

### Run the server in a container

```sh
docker run -d \
  --name mcp-git-commit-generator \
  -p 3001:3001 \
  mcp-git-commit-generator
```

The default entrypoint runs:

```sh
mcp-git-commit-generator --transport sse --host 0.0.0.0 --port 3001
```

The server will be available at `http://localhost:3001`.
To override the port or other arguments, pass them after the image name:

```sh
docker run -d \
   --name mcp-git-commit-generator \
   -p 4000:4000 \
   mcp-git-commit-generator --transport sse --host 0.0.0.0 --port 4000
```

---

## Usage ▶️

> If you run the server using Docker, you can skip the steps below and use the Docker container directly.

### Start the MCP Server 🖥️

**Recommended (no install required):**

- Use Docker as described above.

**To run locally (without Docker):**

1. Set up your uv or Python environment as described in the Installation section.
2. From the project root, run:

   ```sh
   # If you have mcp-git-commit-generator installed in your environment
   mcp-git-commit-generator --transport sse
   ```

   or:

   ```sh
   # Using uv
   uv run -m mcp_git_commit_generator --transport sse
   ```

   or:

   ```sh
   # Using Python directly
   python -m mcp_git_commit_generator --transport sse
   ```

   You can specify other options, for example (*the same in all commands above*):

   ```sh
   python -m mcp_git_commit_generator --transport sse --host 0.0.0.0 --port 3001 -v
   ```

   > The server listens on `0.0.0.0:3001` by default when using Docker, or as specified by the options above.

**Note:**

- If you want to use the CLI entrypoint, ensure the package is installed and your environment is activated.
- Do not use positional arguments (e.g., `python -m mcp_git_commit_generator sse`);
always use options like `--transport sse`.
- Available arguments with their values are:
  - `--transport`: Transport type (e.g., `sse`, `stdio`. default: `stdio`).
  - `--host`: Host to bind the server (default: `0.0.0.0`).
  - `--port`: Port to bind the server (default: `3001`).
  - `-v`, `--verbose`: Verbosity level (e.g., `-v`, `-vv`).

### Generate a Commit Message 📝

1. Stage your changes:

   ```sh
   git add <files>
   ```

2. Use the MCP tool to generate a commit message (see your MCP client for details).

   **Tool arguments:**
   - `repo_path` (optional): Path to the target git repository (defaults to current directory).
   - `commit_type` (optional): Conventional commit type (e.g., feat, fix, docs, etc.).
   - `scope` (optional): Scope of the change (e.g., file or module name).

   > How to provide arguments depends on your MCP client. For example, in the Inspector UI, you can enter these
   in the tool input fields.

### Start the Inspector UI 🔎

From the `inspector` directory:

```sh
npm run dev:inspector
```

> The Inspector UI will be available at `http://localhost:5173`.

## Tool Arguments Reference 📑

### `generate_commit_message`

- `repo_path` (str, optional): Path to the git repository. If omitted, uses the current directory.
- `commit_type` (str, optional): Conventional commit type (e.g., feat, fix, docs, style, etc.).
If omitted, the type will be auto-detected.
- `scope` (str, optional): Scope of the change. If omitted, the scope will be auto-detected based on changed files.

### `check_git_status`

- `repo_path` (str, optional): Path to the git repository. If omitted, uses the current directory.

You can provide these arguments via your MCP client or the Inspector UI when running the tools.

## Project Structure 🗂️

```sh
.
├── .gitignore
├── .markdownlint.jsonc
├── .python-version
├── .vscode/                # VSCode configuration
├── LICENSE
├── README.md
├── pyproject.toml          # Python project configuration
├── uv.lock                 # Python dependencies lock file
├── src/                    # Python source code
│   └── mcp_git_commit_generator/
│       ├── __init__.py     # Main entry point
│       ├── __main__.py     # (if present)
│       └── server.py       # Main server implementation
└── inspector/              # Inspector related files
    ├── package.json        # Node.js dependencies
    └── package-lock.json
```

## MCP Server Configuration (`mcp.json`) ⚙️

The `.vscode/mcp.json` file configures how VS Code and related tools connect to your MCP Git Commit Generator server.
This file defines available server transports and their connection details, making it easy to switch between
different modes (SSE or stdio) for development and debugging.

### Example `mcp.json`

```jsonc
{
  "servers": {
    "sse-mcp-git-commit-generator": {
      "type": "sse",
      "url": "http://localhost:3001/sse"
    },
    "stdio-mcp-git-commit-generator": {
      "type": "stdio",
      "command": "${command:python.interpreterPath}",
      "args": ["-m", "mcp_git_commit_generator", "--transport", "stdio"]
    }
  }
}
```

- **sse-mcp-git-commit-generator**: Connects to the MCP server using Server-Sent Events (SSE) at `http://localhost:3001/sse`.
This is the default when running the server with Docker or directly with the `--transport sse` option.
- **stdio-mcp-git-commit-generator**: Connects using standard input/output (stdio), running the server as a subprocess.
This is useful for local development and debugging.

You can add or modify server entries as needed for your workflow. For more information on available transports and arguments,
see the [Usage](#usage-️) section above.

## How to debug the MCP Server 🐞

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

## Default Ports and customizations ⚙️

| Debug Mode | Ports | Definitions | Customizations | Note |
| ---------- | ----- | ------------ | -------------- |-------------- |
| MCP Inspector | 3001 (Server); 5173 and 3000 (Inspector) | [tasks.json](.vscode/tasks.json) | Edit [launch.json](.vscode/launch.json), [tasks.json](.vscode/tasks.json), [\_\_init\_\_.py](src/__init__.py), [mcp.json](.vscode/mcp.json) to change above ports.| N/A |

## Feedback 💬

If you have any feedback or suggestions, please open an issue on the [MCP Git Commit Generator GitHub repository](https://github.com/theoklitosBam7/mcp-git-commit-generator/issues)

## License 📄

MIT License
