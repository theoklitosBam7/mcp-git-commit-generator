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
- [Node.js](https://nodejs.org/en) (for Inspector UI)
- (*Optional - if you prefer uv*) [uv](https://github.com/astral-sh/uv)
- [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

## Installation

1. **Clone the repository:**

   ```sh
   git clone <repo-url>
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

### Start the Inspector UI

From the `inspector` directory:

```sh
npm run dev:inspector
```

- The Inspector UI will be available at `http://localhost:5173`.

## Project Structure

```sh
.
├── pyproject.toml
├── README.md
├── start-mcp-server.sh
├── src/
│   ├── __init__.py
│   └── server.py
└── inspector/
    └── package.json
```

## Development

- Debugging is supported via `debugpy`.
- See `pyproject.toml` for dev dependencies.

## License

Add your license here.
