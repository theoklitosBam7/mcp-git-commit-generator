"""Main entry point for the MCP server."""

import logging
import os
import sys
from typing import Literal, cast

from .server import mcp


def main():
    """Main function to run the MCP server with specified transport type."""
    transport_type = sys.argv[1] if len(sys.argv) > 1 else None
    verbose = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    logger = logging.getLogger(__name__)
    logger.info(
        "Starting MCP server with transport type: %s, verbosity level: %d",
        transport_type,
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
    if transport_type == "sse":
        port = int(os.environ.get("PORT", 3001))
        mcp.settings.port = port
        mcp.settings.host = "127.0.0.1"
        mcp.run(transport="sse")
    elif transport_type == "stdio":
        mcp.run(transport="stdio")
    else:
        logger.error("Invalid transport type. Use 'sse' or 'stdio'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
