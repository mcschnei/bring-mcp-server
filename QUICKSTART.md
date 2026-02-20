# Bring! MCP Server - Quick Start Guide

Get up and running with the Bring! MCP Server in minutes!

## 1. Prerequisites

- Python 3.10+ installed
- A Bring! account ([sign up here](https://www.getbring.com))
- Claude Desktop installed

## 2. Installation

```bash
# Clone or download the repository
cd bring-mcp-server

# Install the package
pip install -e .

# Verify installation
python -m bring_mcp_server.server --help
```

## 3. Get Your Bring! Credentials

You'll need:
- Your Bring! email address
- Your Bring! password

## 4. Configure Claude Desktop

Find your Python path first:

**macOS:**
```bash
which python3
# Example output: /opt/homebrew/bin/python3
```

**Linux:**
```bash
which python3
# Example output: /usr/bin/python3
```

**Windows:**
```cmd
where python
# Example output: C:\Users\YourName\AppData\Local\Programs\Python\Python310\python.exe
```

### Edit Claude Desktop Config

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/claude/claude_desktop_config.json`

Add this configuration (replace with your Python path and credentials):

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

## 5. Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect.

## 6. Test the Connection

In Claude Desktop, try:

```
Show me all my Bring! shopping lists
```

If configured correctly, Claude will use the `bring_get_lists` tool to fetch your lists!

## Common Issues

### Authentication Error

**Problem:** "BRING_EMAIL and BRING_PASSWORD environment variables must be set"

**Solution:** 
- Verify your credentials are correct in the config file
- Make sure there are no extra spaces or quotes
- Try logging into the Bring! app to confirm your account works

### Python Not Found

**Problem:** "Command not found" or "python not recognized"

**Solution:**
- Double-check your Python path using the commands above
- Ensure Python 3.10+ is installed: `python3 --version`
- Use the full absolute path to Python

### Server Not Appearing

**Problem:** Tools don't show up in Claude

**Solution:**
- Completely quit Claude Desktop (not just close the window)
- Wait a few seconds
- Restart Claude Desktop
- Check Claude Desktop logs for errors

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- See [EXAMPLES.md](EXAMPLES.md) for usage examples
- Check available tools with: "What Bring! tools do you have access to?"

## Quick Examples

```
# View all lists
Show me my shopping lists

# Add items
Add milk, eggs, and bread to my weekly shopping list

# View list contents
What's on my grocery list?

# Complete items
Mark milk as purchased

# Remove items
Remove eggs from my list
```

## Getting Help

- GitHub Issues: [Report a problem](https://github.com/yourusername/bring-mcp-server/issues)
- Bring! API Docs: [bring-api documentation](https://miaucl.github.io/bring-api/)

## Security Reminder

⚠️ **Never commit or share your config file with credentials!**

Keep your `claude_desktop_config.json` secure and private.
