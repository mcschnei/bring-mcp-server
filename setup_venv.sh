#!/bin/bash
# Complete setup script for Bring! MCP Server with virtual environment

set -e

echo "🛒 Bring! MCP Server - Virtual Environment Setup"
echo "================================================"
echo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "📍 Working directory: $SCRIPT_DIR"
echo

# Step 1: Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment already exists at: $VENV_DIR"
else
    echo "1️⃣ Creating virtual environment..."
    /opt/homebrew/bin/python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created"
fi

echo

# Step 2: Activate and install dependencies
echo "2️⃣ Installing dependencies..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install mcp bring-api aiohttp pydantic

echo "✅ Dependencies installed"
echo

# Step 3: Install the package if we're in the package directory
if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
    echo "3️⃣ Installing bring-mcp-server package..."
    pip install -e "$SCRIPT_DIR"
    echo "✅ Package installed"
else
    echo "3️⃣ Skipping package installation (not in package directory)"
fi

echo
echo "================================================"
echo "✅ Setup complete!"
echo
echo "Virtual environment location:"
echo "  $VENV_DIR"
echo
echo "Python executable for Claude Desktop:"
echo "  $VENV_DIR/bin/python3"
echo
echo "Next steps:"
echo "1. Copy the path above: $VENV_DIR/bin/python3"
echo "2. Update your Claude Desktop config:"
echo "   File: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo
echo '   {
     "mcpServers": {
       "bring": {
         "command": "'$VENV_DIR/bin/python3'",
         "args": ["-m", "bring_mcp_server.server"],
         "env": {
           "BRING_EMAIL": "your-email@example.com",
           "BRING_PASSWORD": "your-password"
         }
       }
     }
   }'
echo
echo "3. Restart Claude Desktop"
echo
echo "To verify installation:"
echo "  $VENV_DIR/bin/python3 -c 'import bring_mcp_server; print(bring_mcp_server.__version__)'"
echo
