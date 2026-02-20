# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-02-11

### Added
- Initial release of Bring! MCP Server
- Core shopping list management tools:
  - `bring_get_lists` - Get all shopping lists
  - `bring_get_list_items` - Get items from a specific list
  - `bring_add_item` - Add item to list
  - `bring_complete_item` - Mark item as completed
  - `bring_remove_item` - Remove item from list
  - `bring_batch_update_items` - Batch operations on multiple items
- User information tools:
  - `bring_get_user_info` - Get user account information
  - `bring_get_list_details` - Get detailed list information
- Item catalog tools:
  - `bring_get_item_details` - Get details for specific items
  - `bring_get_all_item_details` - Get complete item catalog
- Comprehensive documentation:
  - README.md with installation and configuration
  - QUICKSTART.md for quick setup
  - EXAMPLES.md with practical usage examples
  - CONTRIBUTING.md for contributors
- Automated setup script
- Basic test suite with pytest
- Support for environment variable configuration
- Claude Desktop integration guide

### Security
- Environment variable-based credential storage
- No hardcoded credentials in code

## [0.0.1] - 2025-02-11

### Added
- Project structure initialization
- Basic package setup
- License (MIT)

[Unreleased]: https://github.com/yourusername/bring-mcp-server/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/bring-mcp-server/releases/tag/v0.1.0
[0.0.1]: https://github.com/yourusername/bring-mcp-server/releases/tag/v0.0.1
