#!/usr/bin/env python3

# See <https://code-maven.com/using-templates-in-flask>
from flask import Flask, request, jsonify, g, Response
import requests
import json
import datetime
import logging
import boto3
from boto3.dynamodb.conditions import Key
import uuid
from pprint import pprint
from dynamodb_operations import create_directMessages_table, create_items, delete_directMessages_table
from botocore.exceptions import ClientError
import decimal

app = Flask(__name__)
endpoint_url= "http://localhost:8000"
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

@app.cli.command('init')
def init_db():
    with app.app_context():
        app.logger.info('inside direct messaging')
        #delete_directMessages_table()
        direct_mesages_table = create_directMessages_table()
        create_items(direct_mesages_table)
        
#This class is used for encoding decimals to integers when dumping a list to JSON:
#Inspired from "https://www.reddit.com/r/aws/comments/bwvio8/dynamodb_has_been_storing_integers_as/"
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

@app.route('/listRepliesTo',methods=['GET'])
def listRepliesTo(dynamodb=None):
    query_parameters=request.args
    messageId=query_parameters.get('messageId')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    
    table = dynamodb.Table('directMessages') 
    scan_kwargs = {
        'FilterExpression': Key('in-reply-to').eq(messageId)
    }
    response = table.scan(**scan_kwargs)
    app.logger.info(response['Items'])
    return json.dumps(response['Items'], cls=DecimalEncoder)

@app.route('/listDirectMessagesFor',methods=['GET'])
def listDirectMessagesFor(dynamodb=None):
    query_parameters=request.args
    username=query_parameters.get('username')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
    
    table = dynamodb.Table('directMessages') 
    scan_kwargs = {
        'FilterExpression': Key('to').eq(username)
    }
    response = table.scan(**scan_kwargs)
    app.logger.info(response['Items'])
    return json.dumps(response['Items'], cls=DecimalEncoder)

@app.route('/sendDirectMessage', methods=['POST'])
def sendDirectMessage(dynamodb=None):
    query_parameters = request.form

    to = query_parameters.get('to')
    messageFrom = query_parameters.get('from')
    message = query_parameters.get('message')
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

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


@app.route('/replyToDirectMessage', methods=['POST'])
def replyToDirectMessage(dynamodb=None):
    query_parameters = request.form

    inReplyToMessageId = query_parameters.get('in-reply-to')
    app.logger.info(query_parameters.get('in-reply-to'))
    if 'quick-reply' in query_parameters and 'quick-replies' in query_parameters:
        quickReply = query_parameters.get('quick-reply')
        quickReplies = query_parameters.get('quick-replies')
        if quickReply != None and quickReply != '' and quickReplies:
            message = { "quick-reply": quickReply, "quickReplies": quickReplies }
    else:
        message = query_parameters.get('reply')
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)

    table = dynamodb.Table('directMessages')
    messageId = uuid.uuid4().hex
     
    try: 
        if inReplyToMessageId == '' or inReplyToMessageId == None or message == '' or message == None:
            return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter(s)" })
        else:
            response = table.put_item(
            Item={
                    'messageId': messageId,
                    'in-reply-to': inReplyToMessageId,
                    'message' : message,
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


