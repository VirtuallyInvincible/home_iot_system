import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LEDState')

iot_client = boto3.client(
    'iot-data', 
    region_name='us-east-1', 
    # I won't tell you my endpoint...
    endpoint_url='https://<iot-endpoint>.amazonaws.com'
)

def lambda_handler(event, context):
    response = table.get_item(Key={'ConfigKey': 'Partition_1'})
    item = response.get('Item', {})
    isLEDOn = item.get('IsLEDOn', False)
    newState = not isLEDOn

    try:
        response = iot_client.publish(
            topic='device/led/state',
            qos=1,
            payload=json.dumps({
                'state': newState,
                'message': 'LED Toggled via Web App'
            })
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Failed to push notification: {str(e)}")
        }
        
    table.put_item(
        Item={
            'ConfigKey': 'Partition_1',
            'IsLEDOn': newState
        }
    )
    
    return {
        'statusCode': 200,
        'body': f"The LED is now {'on' if newState else 'off'}"
    }