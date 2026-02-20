"""
Basic tests for the Bring! MCP Server
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os


@pytest.fixture
def mock_env():
    """Mock environment variables."""
    with patch.dict(os.environ, {
        'BRING_EMAIL': 'test@example.com',
        'BRING_PASSWORD': 'testpassword'
    }):
        yield


@pytest.fixture
def mock_bring():
    """Mock Bring API client."""
    mock = AsyncMock()
    mock.login = AsyncMock()
    mock.load_lists = AsyncMock(return_value={
        'lists': [
            {
                'name': 'Test List',
                'listUuid': 'test-uuid-123',
                'theme': 'default'
            }
        ]
    })
    mock.get_list = AsyncMock(return_value={
        'purchase': [
            {'name': 'Milk', 'specification': 'low fat', 'uuid': 'item-1'}
        ],
        'recently': []
    })
    mock.save_item = AsyncMock()
    mock.complete_item = AsyncMock()
    mock.remove_item = AsyncMock()
    mock.batch_update_list = AsyncMock()
    mock.get_user_account = AsyncMock(return_value={
        'email': 'test@example.com',
        'userUuid': 'user-123',
        'name': 'Test User'
    })
    return mock


@pytest.mark.asyncio
async def test_get_lists(mock_env, mock_bring):
    """Test getting shopping lists."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        client = await get_bring_client()
        assert client is not None
        
        # Call the tool
        result = await call_tool('bring_get_lists', {})
        
        assert len(result) == 1
        assert 'Test List' in result[0].text
        assert 'test-uuid-123' in result[0].text


@pytest.mark.asyncio
async def test_add_item(mock_env, mock_bring):
    """Test adding an item to a list."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        await get_bring_client()
        
        # Call the tool
        result = await call_tool('bring_add_item', {
            'list_uuid': 'test-uuid-123',
            'item_name': 'Bread',
            'specification': 'whole wheat'
        })
        
        assert len(result) == 1
        assert 'Successfully added' in result[0].text
        assert 'Bread' in result[0].text
        
        # Verify the mock was called
        mock_bring.save_item.assert_called_once_with(
            'test-uuid-123',
            'Bread',
            'whole wheat'
        )


@pytest.mark.asyncio
async def test_complete_item(mock_env, mock_bring):
    """Test completing an item."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        await get_bring_client()
        
        # Call the tool
        result = await call_tool('bring_complete_item', {
            'list_uuid': 'test-uuid-123',
            'item_name': 'Milk'
        })
        
        assert len(result) == 1
        assert 'completed' in result[0].text.lower()
        
        # Verify the mock was called
        mock_bring.complete_item.assert_called_once_with(
            'test-uuid-123',
            'Milk'
        )


@pytest.mark.asyncio
async def test_remove_item(mock_env, mock_bring):
    """Test removing an item."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        await get_bring_client()
        
        # Call the tool
        result = await call_tool('bring_remove_item', {
            'list_uuid': 'test-uuid-123',
            'item_name': 'Eggs'
        })
        
        assert len(result) == 1
        assert 'removed' in result[0].text.lower()
        
        # Verify the mock was called
        mock_bring.remove_item.assert_called_once_with(
            'test-uuid-123',
            'Eggs'
        )


@pytest.mark.asyncio
async def test_get_user_info(mock_env, mock_bring):
    """Test getting user information."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        await get_bring_client()
        
        # Call the tool
        result = await call_tool('bring_get_user_info', {})
        
        assert len(result) == 1
        assert 'test@example.com' in result[0].text
        assert 'Test User' in result[0].text


@pytest.mark.asyncio
async def test_missing_credentials():
    """Test that missing credentials raises an error."""
    with patch.dict(os.environ, {}, clear=True):
        from bring_mcp_server.server import get_bring_client
        
        with pytest.raises(ValueError, match="BRING_EMAIL and BRING_PASSWORD"):
            await get_bring_client()


@pytest.mark.asyncio
async def test_invalid_tool_name(mock_env, mock_bring):
    """Test calling an invalid tool."""
    with patch('bring_mcp_server.server.Bring', return_value=mock_bring):
        from bring_mcp_server.server import get_bring_client, call_tool
        
        # Get client
        await get_bring_client()
        
        # Call invalid tool
        result = await call_tool('invalid_tool', {})
        
        assert len(result) == 1
        assert 'Error' in result[0].text
