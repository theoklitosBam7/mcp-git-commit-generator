"""Main entry point for the MCP server."""

import logging
import os
import sys
from typing import Literal, cast

import click

from .server import mcp


@click.command()
@click.option(
    "--transport",
    default="stdio",
    type=click.Choice(["stdio", "sse"]),
    help="Transport type (stdio or sse)",
)
@click.option("--host", default="0.0.0.0", help="Host to listen on (for sse)")
@click.option("--port", default=3001, type=int, help="Port to listen on (for sse)")
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Verbosity level, use -v or -vv",
)
def main(
    transport,
    host,
    port,
    verbose,
):
    """Main function to run the MCP server with specified transport type."""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    logger = logging.getLogger(__name__)
    logger.info(
        "Starting MCP server with transport type: %s, verbosity level: %d",
        transport,
        verbose,
    )

    allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    env_log_level = cast(
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        os.environ.get("LOG_LEVEL", "DEBUG"),
    )
    mcp.settings.log_level = (
        env_log_level if env_log_level in allowed_levels else "DEBUG"
    )
    if transport == "sse":
        mcp.settings.port = port
        mcp.settings.host = host
        mcp.run(transport="sse")
    elif transport == "stdio":
        mcp.run(transport="stdio")
    else:
        logger.error("Invalid transport type. Use 'sse' or 'stdio'.")
        sys.exit(1)


if __name__ == "__main__":
    main(transport="stdio", host=None, port=None, verbose=False)
