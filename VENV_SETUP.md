# Fix: Externally-Managed-Environment Error

## The Problem

Modern Python (via Homebrew) is protected against system-wide package installations to prevent breaking your system. This is the error you're seeing:

```
error: externally-managed-environment
```

## The Solution: Use a Virtual Environment

A virtual environment is an isolated Python environment that won't interfere with your system Python.

## Step-by-Step Setup

### Option 1: Automated Setup (Recommended - Easiest!)

1. **Extract the package** to a permanent location:
   ```bash
   cd ~/Downloads
   unzip bring-mcp-server.zip
   mv bring-mcp-server ~/Projects/
   cd ~/Projects/bring-mcp-server
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup_venv.sh
   ./setup_venv.sh
   ```

3. **Copy the Python path shown** (it will look like):
   ```
   /Users/marco/Projects/bring-mcp-server/.venv/bin/python3
   ```

4. **Update Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "bring": {
         "command": "/Users/marco/Projects/bring-mcp-server/.venv/bin/python3",
         "args": ["-m", "bring_mcp_server.server"],
         "env": {
           "BRING_EMAIL": "your-email@example.com",
           "BRING_PASSWORD": "your-password"
         }
       }
     }
   }
   ```
   
   **Important:** Replace `/Users/marco/Projects/bring-mcp-server/.venv/bin/python3` with the actual path from step 3.

5. **Restart Claude Desktop** (⌘Q then reopen)

### Option 2: Manual Setup

If you prefer to do it manually:

```bash
# 1. Navigate to your bring-mcp-server directory
cd ~/Projects/bring-mcp-server

# 2. Create virtual environment
/opt/homebrew/bin/python3 -m venv .venv

# 3. Activate it
source .venv/bin/activate

# 4. Install dependencies
pip install mcp bring-api aiohttp pydantic

# 5. Install the package
pip install -e .

# 6. Verify
python -c "import bring_mcp_server; print('✅ Success!')"
```

Then use `.venv/bin/python3` in your Claude config (full path).

### Option 3: Standalone Server with Venv

Use the standalone server with a minimal virtual environment:

```bash
# 1. Create a directory
mkdir -p ~/bring-mcp
cd ~/bring-mcp

# 2. Create virtual environment
/opt/homebrew/bin/python3 -m venv .venv

# 3. Activate and install
source .venv/bin/activate
pip install mcp bring-api aiohttp pydantic

# 4. Copy the standalone server
cp ~/Downloads/bring_server_standalone.py ~/bring-mcp/

# 5. Test it
python bring_server_standalone.py
```

Claude Desktop config:
```json
{
  "mcpServers": {
    "bring": {
      "command": "/Users/marco/bring-mcp/.venv/bin/python3",
      "args": ["/Users/marco/bring-mcp/bring_server_standalone.py"],
      "env": {
        "BRING_EMAIL": "your-email@example.com",
        "BRING_PASSWORD": "your-password"
      }
    }
  }
}
```

## Why Virtual Environments?

Virtual environments:
- ✅ Don't interfere with system Python
- ✅ Keep dependencies isolated per project
- ✅ Are the recommended way to manage Python projects
- ✅ Can be deleted and recreated easily
- ✅ Don't require admin/sudo permissions

## Understanding the Paths

After creating a virtual environment at `~/Projects/bring-mcp-server/.venv`:

```
~/Projects/bring-mcp-server/
├── .venv/                          # Virtual environment
│   ├── bin/
│   │   └── python3                 # Use THIS in Claude config
│   └── lib/
│       └── python3.x/
│           └── site-packages/      # Packages installed here
├── src/
│   └── bring_mcp_server/
└── pyproject.toml
```

The Python at `.venv/bin/python3` is a complete, isolated Python installation with its own packages.

## Common Mistakes

### ❌ Wrong: Using system Python
```json
{
  "command": "/opt/homebrew/bin/python3"  // This won't have your packages
}
```

### ✅ Correct: Using venv Python
```json
{
  "command": "/Users/marco/Projects/bring-mcp-server/.venv/bin/python3"
}
```

## Verification

After setup, verify everything works:

```bash
# Check the virtual environment Python has the packages
~/Projects/bring-mcp-server/.venv/bin/python3 -c "
import bring_mcp_server
import bring_api
import mcp
print('✅ All packages found!')
print(f'bring-mcp-server version: {bring_mcp_server.__version__}')
"
```

Expected output:
```
✅ All packages found!
bring-mcp-server version: 0.1.0
```

## Troubleshooting

### "No module named 'bring_mcp_server'"

Even with venv, you still get this error? Check:

```bash
# Are you using the right Python?
which python3  # Should show .venv/bin/python3 when activated

# Is the package installed?
pip list | grep bring-mcp-server

# If not, install it:
pip install -e .
```

### "Command not found: source"

On some shells, use `.` instead:
```bash
. .venv/bin/activate
```

### Virtual environment activation not persisting

You don't need to activate the venv manually. Claude Desktop will use the full path to the venv's Python directly.

## Alternative: Using pipx (Advanced)

If you want a completely isolated installation:

```bash
# Install pipx
brew install pipx

# Install the package (from directory)
cd ~/Projects/bring-mcp-server
pipx install -e .

# Find where pipx installed it
pipx list --include-pipx
```

Then use the Python path from pipx in your Claude config.

## What the Setup Script Does

The `setup_venv.sh` script:
1. Creates a virtual environment at `.venv`
2. Installs all dependencies
3. Installs the bring-mcp-server package
4. Shows you the exact Python path to use
5. Provides a ready-to-use config snippet

## Summary

**Easiest path forward:**

1. Download the package and setup script
2. Run `./setup_venv.sh`
3. Copy the Python path it shows
4. Update Claude Desktop config with that path
5. Restart Claude Desktop

That's it! The virtual environment handles all the complexity.
