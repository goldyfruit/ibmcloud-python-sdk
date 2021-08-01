import json
import os
import re
from tests.constants import FOLDERS, UUID_REGEXP

def get_headers(url, key):
    return {'Content-Type': 'application/json'}

def get_one(path):
    for key, value in FOLDERS.items():
        if path == key:
            data_file = f'{os.path.dirname(__file__)}/{value}/{key}.json'
            with open(data_file, 'r') as json_file:
                try:
                    return {"data": json.load(json_file)[key][0]}
                except json.JSONDecodeError as err:
                    return err

    return {'error': 'unable to read data'}

def get_all(path):
    is_uuid = re.findall(UUID_REGEXP, path)
    uri = None

    if is_uuid:
        #/v1/subnets/...
        uri = re.match(r'/v1/([^/]+)', path).group(1)
    else:
        #/v1/subnets?...
        uri = re.match(r'/v1/(.*)\?', path).group(1)

    for key, value in FOLDERS.items():
        if uri == key:
            data_file = f'{os.path.dirname(__file__)}/{value}/{key}.json'
            with open(data_file, 'r') as json_file:
                try:
                    if is_uuid:
                        return {'data': json.load(json_file)[key][0]}
                    return {'data': json.load(json_file)}
                except json.JSONDecodeError as err:
                    return err

    return {'error': 'unable to read data'}

def qw(conn_type, method, path, headers=None, payload=None):
    return get_all(path)

def qw_not_found(conn_type, method, path, headers=None, payload=None):
    return  {'data': {
                'errors': [{
                    'code': 'not_found',
                    'message': 'Resource not found'
                }]
            }}

def qw_api_error(conn_type, method, path, headers=None, payload=None):
    return  {'data': {
                'errors': [{
                    'code': 'unpredictable_error',
                    'message': 'API call not performed as expected'
                }]
            }}

def qw_exception(conn_type, method, path, headers=None, payload=None):
    raise Exception