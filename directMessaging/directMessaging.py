#!/usr/bin/env python3

# See <https://code-maven.com/using-templates-in-flask>
from flask import Flask, request, jsonify, g
import requests
import datetime
import logging
import boto3
import uuid
from pprint import pprint
from dynamodb_operations import create_directMessages_table, create_items, delete_directMessages_table
from botocore.exceptions import ClientError

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

@app.cli.command('init')
def init_db():
    with app.app_context():
        app.logger.info('inside direct messaging')
        #delete_directMessages_table()
        direct_mesages_table = create_directMessages_table()
        create_items(direct_mesages_table)
        
def get_directMessage(messageId, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('directMessages')

    try:
        response = table.get_item(Key={'messageId': messageId})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

@app.route('/sendDirectMessage', methods=['POST'])
def sendDirectMessage(dynamodb=None):
    query_parameters = request.form

    to = query_parameters.get('to')
    messageFrom = query_parameters.get('from')
    message = query_parameters.get('message')
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('directMessages')
    messageId = uuid.uuid4().hex
     
    try: 
        if to == '' or to == None or messageFrom == None or messageFrom == '' or message == None or message == '':
            return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter(s)" })
        else:
            response = table.put_item(
            Item={
                    'messageId': messageId,
                    'to': to,
                    'from': messageFrom,
                    'message': message,
                    'timestamp': datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") #timestamp datatype not supported in dynamodb so converting it to string
                }
            )
    except requests.exceptions.RequestException as e:
        return flask.json.jsonify({
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        })
    return response


if __name__ == '__main__':
    directMessage = get_directMessage("101")
    if directMessage:
        print("Get directMessage succeeded:")
        pprint(directMessage)