#!/bin/bash
# Launcher script for Bring! MCP Server
# This script activates the virtual environment and runs the server

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/.venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR" >&2
    echo "Please run setup_venv.sh first" >&2
    exit 1
fi

# Use the virtual environment's Python directly
exec "$VENV_DIR/bin/python3" -m bring_mcp_server.server
