#!/usr/bin/env python
from flask import Flask, request, jsonify
from waitress import serve
import os

from function import handler

app = Flask(__name__)

class Event:
    def __init__(self):
        self.body = request.get_data()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path

class Context:
    def __init__(self):
        self.hostname = os.getenv('HOSTNAME', 'localhost')

def format_status_code(res):
    if 'statusCode' in res:
        return res['statusCode']
    
    return 200

def format_body(res):
    if 'body' not in res:
        return ""
    elif isinstance(res['body'], (bytes, str)):
        return res['body']
    else:
        return jsonify(res['body'])

def format_headers(res):
    if 'headers' not in res:
        return []
    elif isinstance(res['headers'], dict):
        headers = []
        for key in res['headers'].keys():
            header_tuple = (key, res['headers'][key])
            headers.append(header_tuple)
        return headers
    
    return res['headers']

def format_response(res):
    if res == None:
        return ('', 200)

    statusCode = format_status_code(res)
    body = format_body(res)
    headers = format_headers(res)

    return (body, statusCode, headers)

@app.route('/', defaults={'path': ''}, methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def call_handler(path):
    event = Event()
    context = Context()
    response_data = handler.handle(event, context)
    
    res = format_response(response_data)
    return res

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
