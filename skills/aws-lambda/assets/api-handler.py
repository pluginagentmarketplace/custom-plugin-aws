"""
AWS Lambda API Handler Template
Complete REST API handler with validation and error handling
"""
import json
import logging
from typing import Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_response(status_code: int, body: Any, headers: dict = None) -> dict:
    """Create standardized API response"""
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            **(headers or {})
        },
        'body': json.dumps(body) if not isinstance(body, str) else body
    }
    return response


def lambda_handler(event: dict, context) -> dict:
    """
    Main Lambda handler for API Gateway events

    Supports:
    - GET /items - List all items
    - GET /items/{id} - Get single item
    - POST /items - Create item
    - PUT /items/{id} - Update item
    - DELETE /items/{id} - Delete item
    """
    logger.info(f"Event: {json.dumps(event)}")

    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return create_response(200, '')

    try:
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        path_params = event.get('pathParameters') or {}
        query_params = event.get('queryStringParameters') or {}
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}

        # Route handling
        if http_method == 'GET' and path == '/items':
            return handle_list_items(query_params)

        elif http_method == 'GET' and 'id' in path_params:
            return handle_get_item(path_params['id'])

        elif http_method == 'POST' and path == '/items':
            return handle_create_item(body)

        elif http_method == 'PUT' and 'id' in path_params:
            return handle_update_item(path_params['id'], body)

        elif http_method == 'DELETE' and 'id' in path_params:
            return handle_delete_item(path_params['id'])

        else:
            return create_response(404, {'error': 'Not found'})

    except json.JSONDecodeError:
        return create_response(400, {'error': 'Invalid JSON'})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})


def handle_list_items(query_params: dict) -> dict:
    """List all items with optional pagination"""
    limit = int(query_params.get('limit', 10))
    offset = int(query_params.get('offset', 0))

    # TODO: Replace with actual database query
    items = [
        {'id': '1', 'name': 'Item 1'},
        {'id': '2', 'name': 'Item 2'},
    ]

    return create_response(200, {
        'items': items[offset:offset + limit],
        'total': len(items)
    })


def handle_get_item(item_id: str) -> dict:
    """Get single item by ID"""
    # TODO: Replace with actual database query
    item = {'id': item_id, 'name': f'Item {item_id}'}

    if not item:
        return create_response(404, {'error': 'Item not found'})

    return create_response(200, item)


def handle_create_item(body: dict) -> dict:
    """Create new item"""
    if not body.get('name'):
        return create_response(400, {'error': 'Name is required'})

    # TODO: Replace with actual database insert
    new_item = {'id': '123', 'name': body['name']}

    return create_response(201, new_item)


def handle_update_item(item_id: str, body: dict) -> dict:
    """Update existing item"""
    # TODO: Replace with actual database update
    updated_item = {'id': item_id, **body}

    return create_response(200, updated_item)


def handle_delete_item(item_id: str) -> dict:
    """Delete item by ID"""
    # TODO: Replace with actual database delete
    return create_response(204, '')
