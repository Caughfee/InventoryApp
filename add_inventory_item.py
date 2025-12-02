import json
import boto3
import uuid
from decimal import Decimal

def lambda_handler(event, context):
    # Parse incoming JSON
    try:
        data = json.loads(event['body'])
    except Exception:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide data.")
        }

    # DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    # Unique ID
    unique_id = str(uuid.uuid4())

    # Insert item
    try:
        table.put_item(
            Item={
                'id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'qty_on_hand': int(data['qty_on_hand']),
                'price': Decimal(str(data['price'])),
                'location_id': int(data['location_id'])
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
