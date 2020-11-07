import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    
    table = dynamodb.create_table(
        TableName='directMessages',
        KeySchema=[
            {
                'AttributeName': 'messageId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'quick-reply',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'messageId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'quick-reply',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table

def create_items(table):
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                'messageId': '101',
                'to': 'Sam',
                'from': 'Pavani',
                'timestamp': '2020-10-06 06:03:47.989280',
                'message': 'Hey Sam! The hydroponics vegetation idea that you took up is really inspiring!'
            }
        )
        batch.put_item(
            Item={
                'messageId': '102',
                'to': 'Pavani',
                'from': 'Sam',
                'timestamp': '2020-10-06 06:04:47.986880',
                'in-reply-to': '101',
                'quick-replies': [
                    'Thanks Pavani',
                    'Thanks for your feedback Pavani',
                    'Thanks Pavani! Much love'
                ],
                'quick-reply': 2
            }
        )
        batch.put_item(
            Item={
                'messageId': '103',
                'to': 'Pavani',
                'from': 'Abhi',
                'timestamp': '2020-10-06 06:02:47.989120',
                'message': 'Hey Pavs! Wassup?'
            }
        )
        batch.put_item(
            Item={
                'messageId': '104',
                'to': 'Abhi',
                'from': 'Pavani',
                'timestamp': '2020-10-06 06:03:47.986880',
                'in-reply-to': '103',
                'message': 'Nothing much! I am just watching the designated survivor series'
            }
        )

if __name__ == '__main__':
    direct_mesages_table = create_movie_table()
    print("Table status:", direct_mesages_table.table_status)
    create_items(direct_mesages_table)