#!/usr/bin/env python3
"""
DynamoDB CRUD Operations Helper
Production-ready patterns for common operations
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json
from typing import Any, Dict, List, Optional
from datetime import datetime


class DynamoDBHelper:
    """Helper class for DynamoDB operations"""

    def __init__(self, table_name: str, region: str = None):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def put_item(self, item: Dict[str, Any]) -> Dict:
        """Create or replace an item"""
        # Convert floats to Decimal for DynamoDB
        item = self._convert_floats(item)

        response = self.table.put_item(Item=item)
        return response

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict]:
        """Get a single item by key"""
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def update_item(
        self,
        key: Dict[str, Any],
        updates: Dict[str, Any],
        condition: str = None
    ) -> Dict:
        """Update specific attributes of an item"""
        update_expression = "SET "
        expression_values = {}
        expression_names = {}

        for i, (attr, value) in enumerate(updates.items()):
            placeholder = f":val{i}"
            name_placeholder = f"#attr{i}"

            update_expression += f"{name_placeholder} = {placeholder}, "
            expression_values[placeholder] = self._convert_value(value)
            expression_names[name_placeholder] = attr

        update_expression = update_expression.rstrip(", ")

        params = {
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_values,
            'ExpressionAttributeNames': expression_names,
            'ReturnValues': 'ALL_NEW'
        }

        if condition:
            params['ConditionExpression'] = condition

        response = self.table.update_item(**params)
        return response.get('Attributes')

    def delete_item(self, key: Dict[str, Any]) -> Dict:
        """Delete an item"""
        response = self.table.delete_item(
            Key=key,
            ReturnValues='ALL_OLD'
        )
        return response.get('Attributes')

    def query(
        self,
        pk_value: str,
        pk_name: str = 'PK',
        sk_begins_with: str = None,
        sk_name: str = 'SK',
        index_name: str = None,
        limit: int = None
    ) -> List[Dict]:
        """Query items by partition key with optional sort key prefix"""
        key_condition = Key(pk_name).eq(pk_value)

        if sk_begins_with:
            key_condition &= Key(sk_name).begins_with(sk_begins_with)

        params = {'KeyConditionExpression': key_condition}

        if index_name:
            params['IndexName'] = index_name

        if limit:
            params['Limit'] = limit

        response = self.table.query(**params)
        return response.get('Items', [])

    def scan_with_filter(
        self,
        filter_attr: str,
        filter_value: Any,
        operator: str = 'eq'
    ) -> List[Dict]:
        """Scan table with filter (use sparingly - expensive operation)"""
        filter_map = {
            'eq': Attr(filter_attr).eq(filter_value),
            'contains': Attr(filter_attr).contains(filter_value),
            'begins_with': Attr(filter_attr).begins_with(filter_value),
            'gt': Attr(filter_attr).gt(filter_value),
            'lt': Attr(filter_attr).lt(filter_value),
        }

        response = self.table.scan(
            FilterExpression=filter_map.get(operator)
        )
        return response.get('Items', [])

    def batch_write(self, items: List[Dict]) -> None:
        """Write multiple items in batch (max 25 items)"""
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=self._convert_floats(item))

    def _convert_floats(self, obj: Any) -> Any:
        """Convert floats to Decimal for DynamoDB"""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: self._convert_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats(v) for v in obj]
        return obj

    def _convert_value(self, value: Any) -> Any:
        """Convert a single value for DynamoDB"""
        if isinstance(value, float):
            return Decimal(str(value))
        return value


# Example usage
if __name__ == '__main__':
    helper = DynamoDBHelper('MyTable')

    # Create
    helper.put_item({
        'PK': 'USER#123',
        'SK': 'PROFILE',
        'Name': 'John Doe',
        'Email': 'john@example.com',
        'CreatedAt': datetime.utcnow().isoformat()
    })

    # Read
    user = helper.get_item({'PK': 'USER#123', 'SK': 'PROFILE'})
    print(f"User: {user}")

    # Update
    updated = helper.update_item(
        {'PK': 'USER#123', 'SK': 'PROFILE'},
        {'Name': 'John Smith', 'UpdatedAt': datetime.utcnow().isoformat()}
    )
    print(f"Updated: {updated}")

    # Query
    items = helper.query('USER#123', sk_begins_with='ORDER#')
    print(f"Orders: {items}")

    # Delete
    deleted = helper.delete_item({'PK': 'USER#123', 'SK': 'PROFILE'})
    print(f"Deleted: {deleted}")
