# Quick Fix: Module Not Found Error

## The Problem

```
ModuleNotFoundError: No module named 'bring_mcp_server'
```

This means the package isn't installed in the Python environment that Claude Desktop is using.

## Solution Options

### Option 1: Install with the Correct Python (Recommended)

The key is to use the **exact same Python** that Claude Desktop is using:

```bash
# Navigate to your bring-mcp-server directory
cd ~/path/to/bring-mcp-server

# Install using Claude's Python
/opt/homebrew/bin/python3 -m pip install -e .
```

**Important:** Use `/opt/homebrew/bin/python3` (the same path in your Claude config) instead of just `python3`.

### Option 2: Use the Standalone Server (Fastest)

Use the standalone version that doesn't require package installation:

1. **Download** `bring_server_standalone.py`

2. **Install just the dependencies:**
   ```bash
   /opt/homebrew/bin/python3 -m pip install mcp bring-api aiohttp pydantic
   ```

3. **Update your Claude Desktop config** to use the standalone file:

   ```json
   {
     "mcpServers": {
       "bring": {
         "command": "/opt/homebrew/bin/python3",
         "args": [
           "/Users/marco/path/to/bring_server_standalone.py"
         ],
         "env": {
           "BRING_EMAIL": "your-email@example.com",
           "BRING_PASSWORD": "your-password"
         }
       }
     }
   }
   ```

   Replace `/Users/marco/path/to/bring_server_standalone.py` with the actual path to the file.

4. **Make it executable:**
   ```bash
   chmod +x bring_server_standalone.py
   ```

5. **Restart Claude Desktop**

### Option 3: Fix Package Installation

If you want to use the package version:

1. **Verify you're in the correct directory:**
   ```bash
   cd ~/path/to/bring-mcp-server
   ls -la
   ```
   
   You should see `src/`, `tests/`, `pyproject.toml`, etc.

2. **Install with the correct Python:**
   ```bash
   /opt/homebrew/bin/python3 -m pip install -e .
   ```

3. **Verify installation:**
   ```bash
   /opt/homebrew/bin/python3 -c "import bring_mcp_server; print('Success!')"
   ```

4. **Restart Claude Desktop**

## Verification Steps

Run this diagnostic command:

```bash
/opt/homebrew/bin/python3 -c "import bring_mcp_server; print('✅ Module installed correctly')" || echo "❌ Module not found"
```

If you see ✅, the installation is correct. If you see ❌, follow one of the solutions above.

## Common Mistakes

### ❌ Wrong: Using system python3
```bash
pip3 install -e .  # This installs to system Python, not Homebrew Python
```

### ✅ Correct: Using Claude's Python
```bash
/opt/homebrew/bin/python3 -m pip install -e .  # This installs to Homebrew Python
```

## Quick Diagnostic

Download and run the diagnostic script:

```bash
chmod +x check_install.sh
./check_install.sh
```

This will show you exactly what's wrong and how to fix it.

## Why This Happens

Python can have multiple installations on your Mac:
- System Python: `/usr/bin/python3`
- Homebrew Python: `/opt/homebrew/bin/python3`
- Other versions from pyenv, conda, etc.

Each has its own set of installed packages. Claude Desktop uses `/opt/homebrew/bin/python3`, so packages must be installed there.

## After Fixing

Once the module is installed correctly:

1. Completely quit Claude Desktop (⌘Q)
2. Wait a few seconds
3. Restart Claude Desktop
4. Test with: "Show me my Bring! shopping lists"

## Still Having Issues?

1. Check Claude Desktop logs for more details
2. Run the diagnostic script: `./check_install.sh`
3. Try the standalone server option (fastest solution)

## Logs Location

macOS: `~/Library/Logs/Claude/mcp*.log`

Look for error messages that might give more clues.
