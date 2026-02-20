#!/usr/bin/env python3
"""
Bring! Shopping Lists MCP Server - Standalone Version

This version can be run directly without installing as a package.
Just run: python3 bring_server_standalone.py
"""

import asyncio
import logging
import os
import sys
from typing import Any, Optional
from uuid import uuid4

# Add basic error handling for imports
try:
    import aiohttp
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from bring_api import Bring, BringItemOperation
except ImportError as e:
    print(f"Error: Missing required package: {e}", file=sys.stderr)
    print("\nPlease install dependencies:", file=sys.stderr)
    print("  pip3 install mcp bring-api aiohttp pydantic", file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Important: Use stderr so it appears in Claude Desktop logs
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
app = Server("bring-mcp-server")

# Global session and Bring instance
_session: Optional[aiohttp.ClientSession] = None
_bring: Optional[Bring] = None


async def get_bring_client() -> Bring:
    """Get or create the Bring client instance."""
    global _session, _bring
    
    if _bring is None:
        email = os.getenv("BRING_EMAIL")
        password = os.getenv("BRING_PASSWORD")
        
        if not email or not password:
            error_msg = "BRING_EMAIL and BRING_PASSWORD environment variables must be set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if _session is None:
            _session = aiohttp.ClientSession()
        
        _bring = Bring(_session, email, password)
        
        try:
            await _bring.login()
            logger.info("Successfully logged in to Bring!")
        except Exception as e:
            logger.error(f"Failed to login to Bring: {e}")
            raise
    
    return _bring


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="bring_get_lists",
            description="Get all shopping lists available to the user",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="bring_get_list_items",
            description="Get all items from a specific shopping list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {"type": "string", "description": "The UUID of the shopping list"}
                },
                "required": ["list_uuid"],
            },
        ),
        Tool(
            name="bring_add_item",
            description="Add a new item to a shopping list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {"type": "string", "description": "The UUID of the shopping list"},
                    "item_name": {"type": "string", "description": "The name of the item to add"},
                    "specification": {"type": "string", "description": "Optional specification for the item"},
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_complete_item",
            description="Mark an item as completed/purchased",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {"type": "string", "description": "The UUID of the shopping list"},
                    "item_name": {"type": "string", "description": "The name of the item to complete"},
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_remove_item",
            description="Remove an item from a shopping list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {"type": "string", "description": "The UUID of the shopping list"},
                    "item_name": {"type": "string", "description": "The name of the item to remove"},
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_batch_update_items",
            description="Perform batch operations on multiple items",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {"type": "string", "description": "The UUID of the shopping list"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "itemId": {"type": "string"},
                                "spec": {"type": "string"},
                                "uuid": {"type": "string"},
                            },
                            "required": ["itemId"],
                        },
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["ADD", "COMPLETE", "REMOVE"],
                    },
                },
                "required": ["list_uuid", "items", "operation"],
            },
        ),
        Tool(
            name="bring_get_user_info",
            description="Get user account information",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        bring = await get_bring_client()
        
        if name == "bring_get_lists":
            result = await bring.load_lists()
            lists = result.get("lists", [])
            
            if not lists:
                return [TextContent(type="text", text="No shopping lists found.")]
            
            output = "Shopping Lists:\n\n"
            for lst in lists:
                output += f"Name: {lst.get('name', 'Unnamed')}\n"
                output += f"UUID: {lst.get('listUuid', 'N/A')}\n"
                output += f"Theme: {lst.get('theme', 'default')}\n---\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_get_list_items":
            list_uuid = arguments["list_uuid"]
            items = await bring.get_list(list_uuid)
            
            purchase_items = items.get("purchase", [])
            recent_items = items.get("recently", [])
            
            output = f"Items in list {list_uuid}:\n\n"
            
            if purchase_items:
                output += "=== Active Items ===\n"
                for item in purchase_items:
                    name = item.get("name", "Unknown")
                    spec = item.get("specification", "")
                    output += f"- {name}"
                    if spec:
                        output += f" ({spec})"
                    output += "\n"
                output += "\n"
            
            if recent_items:
                output += "=== Recently Completed ===\n"
                for item in recent_items:
                    output += f"- {item.get('name', 'Unknown')}\n"
            
            if not purchase_items and not recent_items:
                output += "List is empty.\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_add_item":
            list_uuid = arguments["list_uuid"]
            item_name = arguments["item_name"]
            specification = arguments.get("specification", "")
            
            await bring.save_item(list_uuid, item_name, specification)
            
            msg = f"Successfully added '{item_name}'"
            if specification:
                msg += f" ({specification})"
            msg += f" to list {list_uuid}"
            
            return [TextContent(type="text", text=msg)]
        
        elif name == "bring_complete_item":
            list_uuid = arguments["list_uuid"]
            item_name = arguments["item_name"]
            
            await bring.complete_item(list_uuid, item_name)
            
            return [TextContent(
                type="text",
                text=f"Successfully marked '{item_name}' as completed"
            )]
        
        elif name == "bring_remove_item":
            list_uuid = arguments["list_uuid"]
            item_name = arguments["item_name"]
            
            await bring.remove_item(list_uuid, item_name)
            
            return [TextContent(
                type="text",
                text=f"Successfully removed '{item_name}' from list"
            )]
        
        elif name == "bring_batch_update_items":
            list_uuid = arguments["list_uuid"]
            items = arguments["items"]
            operation = arguments["operation"]
            
            if operation == "ADD":
                op = BringItemOperation.ADD
                for item in items:
                    if "uuid" not in item:
                        item["uuid"] = str(uuid4())
            elif operation == "COMPLETE":
                op = BringItemOperation.COMPLETE
            elif operation == "REMOVE":
                op = BringItemOperation.REMOVE
            else:
                raise ValueError(f"Invalid operation: {operation}")
            
            await bring.batch_update_list(list_uuid, items, op)
            
            return [TextContent(
                type="text",
                text=f"Successfully performed {operation} on {len(items)} item(s)"
            )]
        
        elif name == "bring_get_user_info":
            user_info = await bring.get_user_account()
            
            output = "User Information:\n\n"
            output += f"Email: {user_info.get('email', 'N/A')}\n"
            output += f"User UUID: {user_info.get('userUuid', 'N/A')}\n"
            output += f"Name: {user_info.get('name', 'N/A')}\n"
            
            return [TextContent(type="text", text=output)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def cleanup():
    """Cleanup resources on shutdown."""
    global _session, _bring
    
    if _session:
        await _session.close()
        _session = None
    
    _bring = None
    logger.info("Cleanup completed")


async def main():
    """Main entry point for the server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Bring! MCP Server (standalone mode)")
    
    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        finally:
            await cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
