#!/bin/bash
# Diagnostic script for Bring! MCP Server installation

echo "🔍 Bring! MCP Server - Installation Diagnostic"
echo "=============================================="
echo

# Check Python version
echo "1️⃣ Checking Python installation..."
which python3
python3 --version
echo

# Check if bring_mcp_server is installed
echo "2️⃣ Checking if bring_mcp_server is installed..."
python3 -c "import bring_mcp_server; print('✅ Module found:', bring_mcp_server.__version__)" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ bring_mcp_server module NOT found"
    echo
    echo "Checking pip packages..."
    pip3 list | grep bring
    echo
    echo "To fix this, run from the bring-mcp-server directory:"
    echo "  pip3 install -e ."
else
    echo "✅ Module is properly installed"
fi

echo
echo "3️⃣ Checking dependencies..."
python3 -c "import mcp; print('✅ mcp installed')" 2>&1 || echo "❌ mcp not installed"
python3 -c "import bring_api; print('✅ bring_api installed')" 2>&1 || echo "❌ bring_api not installed"
python3 -c "import aiohttp; print('✅ aiohttp installed')" 2>&1 || echo "❌ aiohttp not installed"
python3 -c "import pydantic; print('✅ pydantic installed')" 2>&1 || echo "❌ pydantic not installed"

echo
echo "4️⃣ Python executable used by Claude:"
echo "/opt/homebrew/bin/python3"
/opt/homebrew/bin/python3 --version

echo
echo "5️⃣ Checking if module is available in Claude's Python..."
/opt/homebrew/bin/python3 -c "import bring_mcp_server; print('✅ Module accessible to Claude Python')" 2>&1 || echo "❌ Module NOT accessible to Claude Python"

echo
echo "=============================================="
echo "If you see errors above, follow these steps:"
echo "1. cd to your bring-mcp-server directory"
echo "2. Run: /opt/homebrew/bin/python3 -m pip install -e ."
echo "3. Restart Claude Desktop"
