__author__ = 'zdvitas'
import json


def make_json_error(text):
    return json.dumps({'Status': "Error", 'Message': text})


def make_json(obj):
    return json.dumps(obj)