#!/bin/bash
# Deploy script for Bring! MCP Server

set -e

echo "🛒 Bring! MCP Server - Deployment"
echo "================================="
echo

# Get the target directory
TARGET_DIR="${1:-$PWD}"

if [ "$TARGET_DIR" = "$PWD" ]; then
    echo "Target directory: $TARGET_DIR (current directory)"
else
    echo "Target directory: $TARGET_DIR"
fi

# Check if target exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory does not exist: $TARGET_DIR"
    exit 1
fi

# Source directory (where this script is)
SOURCE_DIR="/home/claude/bring-mcp-server"

echo
echo "Copying files from container to target location..."
echo

# Copy all files
cp -r "$SOURCE_DIR"/* "$TARGET_DIR/"

echo "✅ Files copied successfully!"
echo
echo "Project structure created in: $TARGET_DIR"
echo
echo "Next steps:"
echo "1. cd $TARGET_DIR"
echo "2. pip3 install -e ."
echo "3. Configure your Bring! credentials"
echo "4. Add to Claude Desktop config"
echo
echo "See QUICKSTART.md for detailed instructions."
