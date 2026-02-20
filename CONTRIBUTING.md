# Contributing to Bring! MCP Server

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/bring-mcp-server.git
cd bring-mcp-server
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## Development Workflow

### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and write tests

3. Run tests:
```bash
pytest
```

4. Format code:
```bash
black src/
```

5. Lint code:
```bash
ruff check src/
```

6. Type check:
```bash
mypy src/
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 100)
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions focused and single-purpose

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures for common setup
- Mock external API calls
- Test both success and error cases

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for batch item operations
fix: Handle authentication errors gracefully
docs: Update installation instructions
test: Add tests for list management
refactor: Simplify error handling logic
```

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description of changes

### PR Checklist

- [ ] Tests pass locally
- [ ] Code is formatted with Black
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

## Project Structure

```
bring-mcp-server/
├── src/
│   └── bring_mcp_server/
│       ├── __init__.py          # Package initialization
│       └── server.py             # Main server implementation
├── tests/
│   └── test_server.py            # Test suite
├── docs/                         # Additional documentation
├── pyproject.toml                # Project configuration
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXAMPLES.md                   # Usage examples
└── CONTRIBUTING.md               # This file
```

## Adding New Tools

When adding a new tool to the MCP server:

1. Add the tool definition in `list_tools()`:
```python
Tool(
    name="bring_new_feature",
    description="Clear description of what it does",
    inputSchema={
        "type": "object",
        "properties": {
            "param_name": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param_name"]
    }
)
```

2. Implement the tool handler in `call_tool()`:
```python
elif name == "bring_new_feature":
    param = arguments["param_name"]
    result = await bring.new_method(param)
    return [TextContent(type="text", text=f"Result: {result}")]
```

3. Write tests:
```python
@pytest.mark.asyncio
async def test_new_feature(mock_env, mock_bring):
    # Test implementation
    pass
```

4. Update documentation:
   - Add to README.md tool list
   - Add examples to EXAMPLES.md
   - Update CHANGELOG.md

## Testing with Real API

To test with the actual Bring! API (not recommended for regular testing):

1. Create a test account on Bring!
2. Set environment variables:
```bash
export BRING_EMAIL="test@example.com"
export BRING_PASSWORD="testpassword"
```
3. Run integration tests:
```bash
pytest -m integration
```

**Important:** Never commit real credentials!

## Documentation

### README.md
- Installation instructions
- Configuration guide
- Tool reference
- Basic examples

### QUICKSTART.md
- Quick setup guide
- Common configurations
- First-time user experience

### EXAMPLES.md
- Detailed usage examples
- Real-world scenarios
- Best practices

Keep documentation:
- Clear and concise
- Up-to-date with code
- Example-driven
- User-focused

## Release Process

1. Update version in `pyproject.toml` and `src/bring_mcp_server/__init__.py`
2. Update CHANGELOG.md
3. Create release branch: `git checkout -b release/v0.2.0`
4. Run full test suite
5. Create GitHub release with notes
6. Merge to main

## Getting Help

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones
- Be respectful and constructive

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Keep discussions on-topic

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to:
- Open an issue with the "question" label
- Start a GitHub discussion
- Check the [bring-api documentation](https://miaucl.github.io/bring-api/)

Thank you for contributing! 🎉
