import os
import sys
from typing import Literal, cast
from server import mcp

if __name__ == "__main__":
    """Main entry point"""
    transport_type = sys.argv[1] if len(sys.argv) > 1 else None
    allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    log_level = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    env_log_level = cast(log_level, os.environ.get("LOG_LEVEL", "DEBUG"))
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
        print("Invalid transport type. Use 'sse' or 'stdio'.")
        sys.exit(1)
