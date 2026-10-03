"""Command-line entry point for the MCP Git Commit Generator."""

from __future__ import annotations

import ipaddress
import logging
import os
import sys
from typing import Literal, cast

import click

from .server import mcp

Transport = Literal["stdio", "streamable-http", "sse"]


def _is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@click.command()
@click.option(
    "--transport",
    default="stdio",
    show_default=True,
    type=click.Choice(["stdio", "streamable-http", "sse"]),
    help="MCP transport. Use streamable-http for network serving; SSE is legacy.",
)
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Host to bind for HTTP transports.",
)
@click.option(
    "--port",
    default=3001,
    show_default=True,
    type=click.IntRange(1, 65535),
    help="Port to bind for HTTP transports.",
)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity.")
def main(transport: Transport, host: str, port: int, verbose: int) -> None:
    """Generate Conventional Commit messages from staged Git changes over MCP."""
    logging_level = logging.WARNING
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    configured_level = os.environ.get("LOG_LEVEL", logging.getLevelName(logging_level)).upper()
    if configured_level not in allowed_levels:
        raise click.ClickException(
            "LOG_LEVEL must be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL."
        )

    logging.basicConfig(level=configured_level, stream=sys.stderr)
    logger = logging.getLogger(__name__)
    mcp.settings.log_level = cast(
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], configured_level
    )

    logger.info("Starting MCP server with transport %s", transport)

    if transport == "stdio":
        mcp.run(transport="stdio")
        return

    if not _is_loopback_host(host):
        logger.warning(
            "Binding an unauthenticated MCP server to non-loopback host %s. "
            "Expose it only on a trusted network or behind an authenticated proxy.",
            host,
        )

    if transport == "streamable-http":
        mcp.run(
            transport="streamable-http",
            host=host,
            port=port,
            stateless_http=True,
            json_response=True,
        )
        return

    logger.warning("SSE is a legacy MCP transport; prefer streamable-http.")
    mcp.run(transport="sse", host=host, port=port)


if __name__ == "__main__":
    main()
