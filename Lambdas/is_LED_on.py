import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LEDState')

def lambda_handler(event, content):
    response = table.get_item(Key={'ConfigKey': 'Partition_1'})
    item = response.get('Item', {})
    flag_value = item.get('IsLEDOn', False)
    
    return {
      'statusCode': 200,
      'headers': {
        'Content-Type': 'application/json'
      },
      'body': json.dumps({
        'message': flag_value,
        'input': event
      })
    }