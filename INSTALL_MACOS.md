# Installation Instructions for macOS

## Option 1: Copy Files from the Output (Recommended)

Since the files have been generated in Claude Desktop, you can download them:

1. **Download all the files** from the links above to a folder on your Mac, for example:
   ```bash
   mkdir -p ~/Projects/bring-mcp-server
   cd ~/Projects/bring-mcp-server
   ```

2. **Create the proper directory structure:**
   ```bash
   mkdir -p src/bring_mcp_server
   mkdir -p tests
   ```

3. **Place the files in the correct locations:**
   - `server.py` → `src/bring_mcp_server/server.py`
   - `test_server.py` → `tests/test_server.py`
   - All `.md`, `.txt`, `.toml`, `.ini`, `.sh` files → root directory

4. **Create the `__init__.py` files:**
   ```bash
   echo '"""Bring! Shopping Lists MCP Server."""

__version__ = "0.1.0"' > src/bring_mcp_server/__init__.py

   echo '"""Tests for Bring! MCP Server."""' > tests/__init__.py
   ```

5. **Make setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

6. **Install the package:**
   ```bash
   pip3 install -e .
   ```

## Option 2: Quick Manual Setup

If you just want to test it quickly without installing as a package:

1. **Create a simple directory structure:**
   ```bash
   mkdir -p ~/bring-mcp-server
   cd ~/bring-mcp-server
   ```

2. **Install dependencies directly:**
   ```bash
   pip3 install mcp bring-api aiohttp pydantic
   ```

3. **Download just the `server.py` file** and save it as `bring_server.py`

4. **Create a launcher script** (`run_server.sh`):
   ```bash
   #!/bin/bash
   export BRING_EMAIL="your-email@example.com"
   export BRING_PASSWORD="your-password"
   python3 bring_server.py
   ```

5. **Make it executable:**
   ```bash
   chmod +x run_server.sh
   ```

6. **Configure Claude Desktop** to use this script:
   ```json
   {
     "mcpServers": {
       "bring": {
         "command": "/Users/marco/bring-mcp-server/run_server.sh"
       }
     }
   }
   ```

## Option 3: Use the Complete Package Structure

If you want the full package with tests and documentation:

1. **Download/copy all files maintaining this structure:**
   ```
   bring-mcp-server/
   ├── src/
   │   └── bring_mcp_server/
   │       ├── __init__.py
   │       └── server.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_server.py
   ├── pyproject.toml
   ├── requirements.txt
   ├── setup.sh
   └── ... (all other files)
   ```

2. **Navigate to the directory:**
   ```bash
   cd ~/path/to/bring-mcp-server
   ```

3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   Or manually:
   ```bash
   pip3 install -e .
   ```

## Verification

After installation, verify it works:

```bash
# Check if the package is installed
pip3 list | grep bring-mcp-server

# Try importing it
python3 -c "import bring_mcp_server; print(bring_mcp_server.__version__)"
```

## Claude Desktop Configuration

Find your Python path:
```bash
which python3
```

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bring": {
      "command": "/opt/homebrew/bin/python3",
      "args": [
        "-m",
        "bring_mcp_server.server"
      ],
      "env": {
        "BRING_EMAIL": "your-email@example.com",
        "BRING_PASSWORD": "your-password"
      }
    }
  }
}
```

## Troubleshooting

### "src does not exist" error

This means you're not in the correct directory. Make sure:
1. You're in the `bring-mcp-server` directory
2. The `src/` folder exists
3. Run `ls -la` to verify the structure

### Module not found error

Install dependencies:
```bash
pip3 install mcp bring-api aiohttp pydantic
```

### Permission denied

Make scripts executable:
```bash
chmod +x setup.sh
```

## Need Help?

Check the comprehensive guides:
- **QUICKSTART.md** - Quick setup guide
- **README.md** - Full documentation
- **EXAMPLES.md** - Usage examples
