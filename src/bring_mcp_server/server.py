"""
Bring! Shopping Lists MCP Server

An MCP server implementation for the Bring! Shopping Lists API.
Provides comprehensive access to shopping list management, item operations,
and user information.
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import aiohttp
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import AnyUrl

# Import the Bring API
try:
    from bring_api import Bring, BringItemOperation
except ImportError:
    raise ImportError(
        "bring-api package is required. Install it with: pip install bring-api"
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
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
        # Get credentials from environment variables
        email = os.getenv("BRING_EMAIL")
        password = os.getenv("BRING_PASSWORD")
        
        if not email or not password:
            raise ValueError(
                "BRING_EMAIL and BRING_PASSWORD environment variables must be set"
            )
        
        # Create session if needed
        if _session is None:
            _session = aiohttp.ClientSession()
        
        # Create Bring instance
        _bring = Bring(_session, email, password)
        
        # Login
        try:
            await _bring.login()
            logger.info("Successfully logged in to Bring!")
        except Exception as e:
            logger.error(f"Failed to login to Bring: {e}")
            raise
    
    return _bring


def safe_get_attr(obj: Any, key: str, default: Any = None) -> Any:
    """Safely get attribute or dict key from an object."""
    if hasattr(obj, key):
        return getattr(obj, key)
    elif isinstance(obj, dict):
        return obj.get(key, default)
    return default


# Tool Definitions

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="bring_get_lists",
            description="Get all shopping lists available to the user. Returns list metadata including UUID, name, and theme.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="bring_get_list_items",
            description="Get all items from a specific shopping list. Returns both active (purchase) items and recently completed items.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list to retrieve items from",
                    },
                },
                "required": ["list_uuid"],
            },
        ),
        Tool(
            name="bring_add_item",
            description="Add a new item to a shopping list. Optionally include specifications (e.g., 'low fat', '2 liters').",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list",
                    },
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to add (e.g., 'Milk', 'Apples')",
                    },
                    "specification": {
                        "type": "string",
                        "description": "Optional specification for the item (e.g., 'low fat', '2kg', 'organic')",
                    },
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_complete_item",
            description="Mark an item as completed/purchased on a shopping list. The item moves to the recently completed section.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list",
                    },
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to complete",
                    },
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_remove_item",
            description="Remove an item completely from a shopping list (not just complete it).",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list",
                    },
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to remove",
                    },
                },
                "required": ["list_uuid", "item_name"],
            },
        ),
        Tool(
            name="bring_batch_update_items",
            description="Perform batch operations (ADD, COMPLETE, REMOVE) on multiple items at once. This uses the modern API endpoint and supports unique item identification via UUID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list",
                    },
                    "items": {
                        "type": "array",
                        "description": "Array of items to process. Each item should have 'itemId' (required), 'spec' (optional), and 'uuid' (optional but recommended)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "itemId": {
                                    "type": "string",
                                    "description": "The item name/ID",
                                },
                                "spec": {
                                    "type": "string",
                                    "description": "Optional item specification",
                                },
                                "uuid": {
                                    "type": "string",
                                    "description": "Optional unique identifier for the item (recommended for tracking)",
                                },
                            },
                            "required": ["itemId"],
                        },
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["ADD", "COMPLETE", "REMOVE"],
                        "description": "The operation to perform on the items",
                    },
                },
                "required": ["list_uuid", "items", "operation"],
            },
        ),
        Tool(
            name="bring_get_user_info",
            description="Get information about the currently authenticated user, including email and user settings.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="bring_get_list_details",
            description="Get detailed information about a specific shopping list, including settings and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_uuid": {
                        "type": "string",
                        "description": "The UUID of the shopping list",
                    },
                },
                "required": ["list_uuid"],
            },
        ),
        Tool(
            name="bring_get_item_details",
            description="Get detailed information about specific items in the catalog, including translations and images.",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of item IDs to get details for",
                    },
                    "locale": {
                        "type": "string",
                        "description": "Optional locale code (e.g., 'en-US', 'de-DE'). Defaults to user's locale",
                    },
                },
                "required": ["item_ids"],
            },
        ),
        Tool(
            name="bring_get_all_item_details",
            description="Get all available items from the Bring catalog with their details, translations, and images.",
            inputSchema={
                "type": "object",
                "properties": {
                    "locale": {
                        "type": "string",
                        "description": "Optional locale code (e.g., 'en-US', 'de-DE'). Defaults to 'en-US'",
                    },
                },
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        bring = await get_bring_client()
        
        if name == "bring_get_lists":
            result = await bring.load_lists()
            lists = safe_get_attr(result, "lists", [])
            
            if not lists:
                return [TextContent(type="text", text="No shopping lists found.")]
            
            output = "Shopping Lists:\n\n"
            for lst in lists:
                name_val = safe_get_attr(lst, 'name', 'Unnamed')
                uuid_val = safe_get_attr(lst, 'listUuid', 'N/A')
                theme_val = safe_get_attr(lst, 'theme', 'default')
                output += f"Name: {name_val}\n"
                output += f"UUID: {uuid_val}\n"
                output += f"Theme: {theme_val}\n"
                output += "---\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_get_list_items":
            list_uuid = arguments["list_uuid"]
            items_response = await bring.get_list(list_uuid)
            
            # The response is BringItemsResponse which has an .items attribute
            # That .items is an Items object with .purchase and .recently attributes
            items_obj = safe_get_attr(items_response, "items")
            
            purchase_items = []
            recent_items = []
            
            if items_obj:
                purchase_items = safe_get_attr(items_obj, "purchase", [])
                recent_items = safe_get_attr(items_obj, "recently", [])
            
            output = f"Items in list {list_uuid}:\n\n"
            
            if purchase_items:
                output += "=== Active Items (To Purchase) ===\n"
                for item in purchase_items:
                    # BringPurchase objects use 'itemId' not 'name', and 'spec' not 'specification'
                    name = safe_get_attr(item, "itemId") or safe_get_attr(item, "name", "Unknown")
                    spec = safe_get_attr(item, "spec") or safe_get_attr(item, "specification", "")
                    uuid = safe_get_attr(item, "uuid", "")
                    output += f"- {name}"
                    if spec:
                        output += f" ({spec})"
                    if uuid:
                        output += f" [UUID: {uuid}]"
                    output += "\n"
                output += "\n"
            
            if recent_items:
                output += "=== Recently Completed ===\n"
                for item in recent_items:
                    name = safe_get_attr(item, "itemId") or safe_get_attr(item, "name", "Unknown")
                    spec = safe_get_attr(item, "spec") or safe_get_attr(item, "specification", "")
                    output += f"- {name}"
                    if spec:
                        output += f" ({spec})"
                    output += "\n"
            
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
                text=f"Successfully marked '{item_name}' as completed in list {list_uuid}"
            )]
        
        elif name == "bring_remove_item":
            list_uuid = arguments["list_uuid"]
            item_name = arguments["item_name"]
            
            await bring.remove_item(list_uuid, item_name)
            
            return [TextContent(
                type="text",
                text=f"Successfully removed '{item_name}' from list {list_uuid}"
            )]
        
        elif name == "bring_batch_update_items":
            list_uuid = arguments["list_uuid"]
            items = arguments["items"]
            operation = arguments["operation"]
            
            # Convert operation string to BringItemOperation enum
            if operation == "ADD":
                op = BringItemOperation.ADD
            elif operation == "COMPLETE":
                op = BringItemOperation.COMPLETE
            elif operation == "REMOVE":
                op = BringItemOperation.REMOVE
            else:
                raise ValueError(f"Invalid operation: {operation}")
            
            # Add UUIDs to items that don't have them (for ADD operations)
            if operation == "ADD":
                for item in items:
                    if "uuid" not in item or not item["uuid"]:
                        item["uuid"] = str(uuid4())
            
            await bring.batch_update_list(list_uuid, items, op)
            
            item_count = len(items)
            return [TextContent(
                type="text",
                text=f"Successfully performed {operation} operation on {item_count} item(s) in list {list_uuid}"
            )]
        
        elif name == "bring_get_user_info":
            user_info = await bring.get_user_account()
            
            output = "User Information:\n\n"
            output += f"Email: {safe_get_attr(user_info, 'email', 'N/A')}\n"
            output += f"User UUID: {safe_get_attr(user_info, 'userUuid', 'N/A')}\n"
            output += f"Name: {safe_get_attr(user_info, 'name', 'N/A')}\n"
            output += f"Photo Path: {safe_get_attr(user_info, 'photoPath', 'N/A')}\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_get_list_details":
            list_uuid = arguments["list_uuid"]
            details = await bring.get_list_details(list_uuid)
            
            output = f"List Details for {list_uuid}:\n\n"
            output += f"Name: {safe_get_attr(details, 'name', 'N/A')}\n"
            output += f"Theme: {safe_get_attr(details, 'theme', 'N/A')}\n"
            
            # Include any additional details if it's a dict
            if isinstance(details, dict):
                for key, value in details.items():
                    if key not in ['name', 'theme', 'listUuid']:
                        output += f"{key}: {value}\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_get_item_details":
            item_ids = arguments["item_ids"]
            locale = arguments.get("locale")
            
            if locale:
                details = await bring.get_items_details(locale)
            else:
                details = await bring.get_items_details()
            
            # Filter to requested items
            filtered_items = [
                item for item in details
                if safe_get_attr(item, "itemId") in item_ids
            ]
            
            if not filtered_items:
                return [TextContent(
                    type="text",
                    text=f"No details found for items: {', '.join(item_ids)}"
                )]
            
            output = "Item Details:\n\n"
            for item in filtered_items:
                output += f"Item: {safe_get_attr(item, 'itemId', 'Unknown')}\n"
                output += f"  Translations: {safe_get_attr(item, 'translations', {})}\n"
                output += f"  Image: {safe_get_attr(item, 'imagePath', 'N/A')}\n"
                output += "---\n"
            
            return [TextContent(type="text", text=output)]
        
        elif name == "bring_get_all_item_details":
            locale = arguments.get("locale", "en-US")
            
            details = await bring.get_items_details(locale)
            
            output = f"All Items (Locale: {locale}):\n\n"
            output += f"Total items: {len(details)}\n\n"
            
            # Show first 50 items to avoid overwhelming output
            for item in details[:50]:
                item_id = safe_get_attr(item, "itemId", "Unknown")
                translations = safe_get_attr(item, "translations", {})
                output += f"- {item_id}"
                if translations:
                    # Show first translation
                    first_trans = next(iter(translations.values()), "")
                    if first_trans:
                        output += f": {first_trans}"
                output += "\n"
            
            if len(details) > 50:
                output += f"\n... and {len(details) - 50} more items"
            
            return [TextContent(type="text", text=output)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


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
    asyncio.run(main())
