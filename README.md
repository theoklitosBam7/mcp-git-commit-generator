# MCP Git Commit Generator

Generate conventional commit messages from your staged git changes using Model Context Protocol (MCP).

## Features

- **Automatic commit message generation** based on staged git diffs.
- Supports [Conventional Commits](https://www.conventionalcommits.org/).
- MCP server with both SSE and stdio transport options.
- Inspector UI for interactive inspection (via MCP Inspector).

## Requirements

- [Python](https://www.python.org/) >= 3.13.5
- [MCP CLI](https://pypi.org/project/mcp/) >= 1.10.1
- (*Optional*) [Node.js](https://nodejs.org/en) (for Inspector UI)
- (*Optional - if you prefer uv*) [uv](https://github.com/astral-sh/uv)
- (*Optional*) [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/theoklitosBam7/mcp-git-commit-generator.git
   cd mcp-git-commit-generator
   ```

2. **Prepare environment**

    There are two approaches to set up the environment for this project. You can choose either one based on your preference.

    > Note: Reload VSCode or terminal to ensure the virtual environment python is used after creating the virtual environment.

    | Approach | Steps |
    | -------- | ----- |
    | Using `uv` | 1. Create virtual environment: `uv venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment <br>3. Install dependencies (include dev dependencies): `uv pip install -r pyproject.toml --group dev` |
    | Using `pip` | 1. Create virtual environment: `python -m venv .venv` <br>2. Run VSCode Command "***Python: Select Interpreter***" and select the python from created virtual environment<br>3. Install dependencies (include dev dependencies): `pip install -e .[dev]` |

3. **(Optional) Install Inspector dependencies:**

   ```sh
   cd inspector
   npm install
   ```

## Usage

### Start the MCP Server

You can start the server using the provided script:

```sh
./start-mcp-server.sh
```

Or manually:

```sh
python ./src/__init__.py sse
```

- The server listens on `127.0.0.1:3001` by default.

### Generate a Commit Message

1. Stage your changes:

   ```sh
   git add <files>
   ```

2. Use the MCP tool to generate a commit message (see your MCP client for details).

   **Tool arguments:**
   - `commit_type` (optional): Conventional commit type (e.g., feat, fix, docs, etc.).
   - `scope` (optional): Scope of the change (e.g., file or module name).
   - `repo_path` (optional): Path to the target git repository (defaults to current directory).

   > How to provide arguments depends on your MCP client. For example, in the Inspector UI, you can enter these
   in the tool input fields.

### Start the Inspector UI

From the `inspector` directory:

```sh
npm run dev:inspector
```

- The Inspector UI will be available at `http://localhost:5173`.

## Tool Arguments Reference

### `generate_commit_message`

- `commit_type` (str, optional): Conventional commit type (e.g., feat, fix, docs, style, etc.).
If omitted, the type will be auto-detected.
- `scope` (str, optional): Scope of the change. If omitted, the scope will be auto-detected based on changed files.
- `repo_path` (str, optional): Path to the git repository. If omitted, uses the current directory.

### `check_git_status`

- `repo_path` (str, optional): Path to the git repository. If omitted, uses the current directory.

You can provide these arguments via your MCP client or the Inspector UI when running the tools.

## Project Structure

```sh
.
├── .gitignore
├── .markdownlint.jsonc
├── .python-version
├── .vscode/              # VSCode configuration
├── LICENSE
├── README.md
├── pyproject.toml        # Python project configuration
├── start-mcp-server.sh   # Script to start the MCP server
├── uv.lock              # Python dependencies lock file
├── src/                  # Python source code
│   ├── __init__.py
│   └── server.py        # Main server implementation
└── inspector/            # Inspector related files
    ├── package.json     # Node.js dependencies
    └── package-lock.json
```

## How to debug the MCP Server

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

## Default Ports and customizations

| Debug Mode | Ports | Definitions | Customizations | Note |
| ---------- | ----- | ------------ | -------------- |-------------- |
| MCP Inspector | 3001 (Server); 5173 and 3000 (Inspector) | [tasks.json](.vscode/tasks.json) | Edit [launch.json](.vscode/launch.json), [tasks.json](.vscode/tasks.json), [\_\_init\_\_.py](src/__init__.py), [mcp.json](.vscode/mcp.json) to change above ports.| N/A |

## Feedback

If you have any feedback or suggestions, please open an issue on the [MCP Git Commit Generator GitHub repository](https://github.com/theoklitosBam7/mcp-git-commit-generator/issues)

## License

MIT License
