#!/bin/bash
# Setup script for Bring! MCP Server

set -e

echo "🛒 Bring! MCP Server Setup"
echo "=========================="
echo

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"
echo

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip."
    exit 1
fi

echo "✅ pip3 found"
echo

# Install the package
echo "Installing Bring! MCP Server..."
pip3 install -e .

if [ $? -eq 0 ]; then
    echo "✅ Installation successful!"
else
    echo "❌ Installation failed"
    exit 1
fi

echo
echo "=========================="
echo "Setup complete! 🎉"
echo
echo "Next steps:"
echo "1. Get your Bring! credentials ready (email and password)"
echo "2. Find your Python path: which python3"
echo "3. Configure Claude Desktop (see QUICKSTART.md)"
echo
echo "For detailed instructions, see:"
echo "  - QUICKSTART.md for quick setup"
echo "  - README.md for full documentation"
echo "  - EXAMPLES.md for usage examples"
echo
