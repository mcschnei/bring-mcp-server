# Bring! Shopping Lists MCP Server

An MCP (Model Context Protocol) server that provides comprehensive access to the Bring! Shopping Lists API. This server allows AI assistants like Claude to manage your shopping lists, add/remove items, and retrieve list information.

## Features

- 🛒 **List Management**: View all your shopping lists with metadata
- ➕ **Add Items**: Add items to lists with optional specifications
- ✅ **Complete Items**: Mark items as purchased
- 🗑️ **Remove Items**: Delete items from lists
- 📦 **Batch Operations**: Perform bulk operations on multiple items
- 👤 **User Info**: Retrieve account information
- 📋 **Item Catalog**: Access the complete Bring! item catalog with translations
- 🔍 **List Details**: Get detailed information about specific lists

## Prerequisites

- Python 3.10 or higher
- A Bring! account (sign up at [getbring.com](https://www.getbring.com))
- Bring! credentials (email and password)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/bring-mcp-server.git
cd bring-mcp-server

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install bring-mcp-server
```

## Configuration

### Environment Variables

Set your Bring! credentials as environment variables:

```bash
export BRING_EMAIL="your-email@example.com"
export BRING_PASSWORD="your-password"
```

Or create a `.env` file:

```
BRING_EMAIL=your-email@example.com
BRING_PASSWORD=your-password
```

### Claude Desktop Configuration

Add the server to your Claude Desktop configuration file:

#### macOS

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

#### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bring": {
      "command": "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Python\\Python310\\python.exe",
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

#### Linux

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bring": {
      "command": "/usr/bin/python3",
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

## Available Tools

### `bring_get_lists`

Get all shopping lists available to the user.

**Parameters:** None

**Example:**
```
Show me all my shopping lists
```

### `bring_get_list_items`

Get all items from a specific shopping list.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list

**Example:**
```
What items are in my weekly shopping list?
```

### `bring_add_item`

Add a new item to a shopping list.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list
- `item_name` (string): The name of the item to add
- `specification` (string, optional): Item specification (e.g., "low fat", "2kg")

**Example:**
```
Add milk (low fat) to my weekly shopping list
```

### `bring_complete_item`

Mark an item as completed/purchased.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list
- `item_name` (string): The name of the item to complete

**Example:**
```
Mark bread as purchased in my weekly list
```

### `bring_remove_item`

Remove an item completely from a shopping list.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list
- `item_name` (string): The name of the item to remove

**Example:**
```
Remove eggs from my shopping list
```

### `bring_batch_update_items`

Perform batch operations on multiple items at once.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list
- `items` (array): Array of item objects with `itemId`, `spec` (optional), and `uuid` (optional)
- `operation` (string): Operation to perform: "ADD", "COMPLETE", or "REMOVE"

**Example:**
```
Add multiple items to my list: apples, oranges, and bananas
```

### `bring_get_user_info`

Get information about the currently authenticated user.

**Parameters:** None

**Example:**
```
Show me my Bring account information
```

### `bring_get_list_details`

Get detailed information about a specific shopping list.

**Parameters:**
- `list_uuid` (string): The UUID of the shopping list

**Example:**
```
Show me details about my weekly shopping list
```

### `bring_get_item_details`

Get detailed information about specific items from the catalog.

**Parameters:**
- `item_ids` (array): Array of item IDs to get details for
- `locale` (string, optional): Locale code (e.g., "en-US", "de-DE")

**Example:**
```
Get details for Milk and Bread items
```

### `bring_get_all_item_details`

Get all available items from the Bring! catalog.

**Parameters:**
- `locale` (string, optional): Locale code (default: "en-US")

**Example:**
```
Show me all available items in the Bring catalog
```

## Usage Examples

### Basic Shopping List Management

```
You: Show me all my shopping lists
Claude: [Calls bring_get_lists and displays all lists]

You: Add milk, eggs, and bread to my weekly shopping list
Claude: [Calls bring_batch_update_items to add all three items]

You: What's on my weekly shopping list?
Claude: [Calls bring_get_list_items and displays all items]

You: Mark milk as purchased
Claude: [Calls bring_complete_item to complete the item]

You: Remove eggs from the list
Claude: [Calls bring_remove_item to delete the item]
```

### Advanced Item Management

```
You: Add 2kg of apples and 1 liter of organic milk to my list
Claude: [Calls bring_batch_update_items with specifications]

You: Get details about the Milk item in the catalog
Claude: [Calls bring_get_item_details with itemId "Milk"]
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Project Structure

```
bring-mcp-server/
├── src/
│   └── bring_mcp_server/
│       ├── __init__.py
│       └── server.py
├── tests/
│   └── test_server.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## Security

- **Never commit credentials**: Always use environment variables or secure configuration
- **Secure storage**: Store your configuration file with appropriate permissions
- **API key security**: Treat your Bring! credentials like passwords

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your Bring! credentials are correct
2. Check that environment variables are properly set
3. Try logging into the Bring! app to ensure your account is active

### Connection Issues

If the server fails to connect:
1. Check your internet connection
2. Verify the Bring! API is accessible
3. Check Claude Desktop logs for detailed error messages

### Finding Python Path

To find your Python executable path:

**macOS/Linux:**
```bash
which python3
```

**Windows:**
```cmd
where python
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is an unofficial implementation and is not endorsed by or affiliated with Bring! Labs AG. Use at your own risk.

## Credits

Built on top of the excellent [bring-api](https://github.com/miaucl/bring-api) Python package by [@miaucl](https://github.com/miaucl) and [@tr4nt0r](https://github.com/tr4nt0r).

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/yourusername/bring-mcp-server/issues)
- Check the [bring-api documentation](https://miaucl.github.io/bring-api/)
