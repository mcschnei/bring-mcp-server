# Bring! MCP Server - Complete Package Installation

## Package Contents

This package contains everything you need to run the Bring! MCP Server:

```
bring-mcp-server/
├── src/
│   └── bring_mcp_server/
│       ├── __init__.py          # Package initialization
│       └── server.py             # Main MCP server (10 tools)
├── tests/
│   ├── __init__.py              # Tests package
│   └── test_server.py            # Test suite
├── README.md                     # Full documentation
├── QUICKSTART.md                 # Quick start guide
├── EXAMPLES.md                   # Usage examples
├── INSTALL_MACOS.md              # macOS specific instructions
├── CONTRIBUTING.md               # Development guide
├── CHANGELOG.md                  # Version history
├── pyproject.toml                # Package configuration
├── requirements.txt              # Dependencies
├── pytest.ini                    # Test configuration
├── setup.sh                      # Unix setup script
├── deploy.sh                     # Deployment helper
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## Installation Methods

### Method 1: Standard Installation (Recommended)

**For macOS/Linux:**

```bash
# Extract the package
cd ~/Downloads  # or wherever you saved the file
tar -xzf bring-mcp-server.tar.gz  # OR: unzip bring-mcp-server.zip

# Move to a permanent location
mv bring-mcp-server ~/Projects/  # or any location you prefer
cd ~/Projects/bring-mcp-server

# Run the setup script
./setup.sh
```

**For Windows:**

```cmd
# Extract the ZIP file to a location like C:\Projects\bring-mcp-server
cd C:\Projects\bring-mcp-server

# Install
pip install -e .
```

### Method 2: Manual Installation

```bash
# Extract the package
unzip bring-mcp-server.zip
# OR
tar -xzf bring-mcp-server.tar.gz

# Navigate to the directory
cd bring-mcp-server

# Install dependencies
pip3 install -r requirements.txt

# Install the package in editable mode
pip3 install -e .
```

### Method 3: Quick Test Without Installation

```bash
# Extract and navigate
unzip bring-mcp-server.zip
cd bring-mcp-server

# Install only the dependencies
pip3 install mcp bring-api aiohttp pydantic

# Set credentials
export BRING_EMAIL="your-email@example.com"
export BRING_PASSWORD="your-password"

# Run directly
python3 -m bring_mcp_server.server
```

## Post-Installation Setup

### 1. Verify Installation

```bash
# Check if installed
pip3 list | grep bring-mcp-server

# Test import
python3 -c "import bring_mcp_server; print(bring_mcp_server.__version__)"
```

Expected output: `0.1.0`

### 2. Get Your Bring! Credentials

- Email address you use for Bring!
- Your Bring! password

### 3. Find Your Python Path

**macOS/Linux:**
```bash
which python3
```

Common outputs:
- `/opt/homebrew/bin/python3` (Homebrew on Apple Silicon)
- `/usr/local/bin/python3` (Homebrew on Intel)
- `/usr/bin/python3` (System Python)

**Windows:**
```cmd
where python
```

### 4. Configure Claude Desktop

Edit the Claude Desktop configuration file:

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```cmd
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/claude/claude_desktop_config.json
```

**Add this configuration:**

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

**Important:** Replace:
- `/opt/homebrew/bin/python3` with YOUR Python path
- `your-email@example.com` with YOUR Bring! email
- `your-password` with YOUR Bring! password

### 5. Restart Claude Desktop

Completely quit Claude Desktop and restart it for the changes to take effect.

### 6. Test the Integration

In Claude Desktop, try:

```
Show me all my Bring! shopping lists
```

If successful, Claude will use the `bring_get_lists` tool!

## Common Issues and Solutions

### Issue: "src does not exist"

**Solution:** Make sure you extracted the complete package and you're in the `bring-mcp-server` directory when running `pip install -e .`

```bash
cd bring-mcp-server
ls -la  # You should see the 'src' directory
pip3 install -e .
```

### Issue: "Module not found: bring_api"

**Solution:** Install dependencies first:

```bash
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install mcp bring-api aiohttp pydantic
```

### Issue: "Command not found: python3"

**Solution:** On some systems, use `python` instead:

```bash
pip install -e .
python -m bring_mcp_server.server
```

Update Claude config to use `python` instead of `python3`.

### Issue: Authentication errors in Claude

**Solution:** 
1. Verify your Bring! credentials are correct
2. Try logging into the Bring! app/website
3. Check for typos in the config file
4. Ensure no extra spaces in email/password

### Issue: Tools not appearing in Claude

**Solution:**
1. Completely quit Claude Desktop (⌘Q on Mac, not just close window)
2. Wait 5 seconds
3. Restart Claude Desktop
4. Check the Claude Desktop logs for errors

### Issue: Permission denied on setup.sh

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

## File Locations

### Configuration File Locations

**macOS:**
- Config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Logs: `~/Library/Logs/Claude/`

**Windows:**
- Config: `%APPDATA%\Claude\claude_desktop_config.json`
- Logs: `%APPDATA%\Claude\logs\`

**Linux:**
- Config: `~/.config/claude/claude_desktop_config.json`
- Logs: `~/.local/share/Claude/logs/`

## Quick Reference

### Available Commands

```bash
# Install
pip3 install -e .

# Run tests
pytest

# Format code
black src/

# Type check
mypy src/

# Lint
ruff check src/
```

### Environment Variables

```bash
# Required
export BRING_EMAIL="your-email@example.com"
export BRING_PASSWORD="your-password"
```

## Documentation

After installation, read:
1. **QUICKSTART.md** - Quick start guide
2. **README.md** - Complete documentation
3. **EXAMPLES.md** - Usage examples
4. **CONTRIBUTING.md** - For developers

## Getting Help

1. Check **QUICKSTART.md** for quick solutions
2. Review **EXAMPLES.md** for usage patterns
3. Read **INSTALL_MACOS.md** for macOS-specific help
4. Open an issue on GitHub

## Next Steps

Once installed and configured:

1. Test basic commands:
   - "Show me my shopping lists"
   - "Add milk to my list"
   - "What's on my grocery list?"

2. Explore advanced features:
   - Batch operations
   - Item catalog browsing
   - Multiple list management

3. Read the examples for inspiration

## Success Checklist

- [ ] Package extracted
- [ ] Dependencies installed
- [ ] Package installed with pip
- [ ] Bring! credentials obtained
- [ ] Python path identified
- [ ] Claude Desktop configured
- [ ] Claude Desktop restarted
- [ ] First test command successful

Congratulations! You're ready to use the Bring! MCP Server! 🎉
