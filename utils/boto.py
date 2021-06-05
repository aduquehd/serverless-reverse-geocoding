import os

import boto3
from boto3.dynamodb.conditions import Key

client = boto3.client('dynamodb')


def create_record(table_name: str, item: dict) -> dict:
    resp = client.put_item(
        TableName=table_name,
        Item=item
    )
    return resp


def get_item(table_name: str, key: dict) -> dict:
    resp = client.get_item(
        TableName=table_name,
        Key=key
    )
    item = resp.get('Item')
    return item


def filter_dynamodb(table_name: str, index_name: str, key_name: str, key_value: str) -> dict:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key(key_name).eq(key_value),
        ScanIndexForward=True
    )
    return response
