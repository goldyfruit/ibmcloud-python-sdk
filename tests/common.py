import json
import os
import re
from types import SimpleNamespace
from tests.constants import FOLDERS, UUID_REGEXP, ID_REGEXP


def get_headers(arg1=None, arg2=None):
    """This function adds hearders that are required by
    ibmcloud_python_sdk.auth.get_token method. arg1 and arg2 are not used.
    """
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaXR'
    }

def read_one(path, key, index=0):
    """This function returns only one item from a given file based on
    a dict name and index.
    """
    data_file = f'{os.path.dirname(__file__)}/{path}'
    with open(data_file, 'r') as json_file:
        try:
            return json.load(json_file)[key][index]
        except json.JSONDecodeError as err:
            return err

def get_one(path, index=0):
    """This function returns only one item of the list. The
    item to return could be selected by using the index variable.
    """
    for key, value in FOLDERS.items():
        if path == key:
            data_dict = key
            if key == 'resource_groups':
                data_dict = 'resources'
            data_file = f'{os.path.dirname(__file__)}/{value}/{key}.json'
            with open(data_file, 'r') as json_file:
                try:
                    return {"data": json.load(json_file)[data_dict][index]}
                except json.JSONDecodeError as err:
                    return err

    return {'error': 'unable to read data'}

def get_all(path, index=0):
    """This function returns all the items from the JSON file except if a
    UUID is detected in the URL path then only one item will be returned.
    """
    is_uuid = re.findall(UUID_REGEXP, path)
    is_id = re.findall(ID_REGEXP, path)
    
    uri = None

    if is_uuid:
        #/v1/subnets/...
        #/v1/subnets/.../...
        uri = re.match(r'/v1/([^/]+)', path).group(1)
    elif is_id:
        #/v2/resource_groups/...
        uri = re.match(r'/v2/([^/]+)', path).group(1)
    else:
        #/v2/resource_groups/...
        if re.match(r'/v2/(.*)', path):
            uri = re.match(r'/v2/(.*)', path).group(1)
        else:
            #/v1/subnets?...
            uri = re.match(r'/v1/(.*)\?', path).group(1)

    for key, value in FOLDERS.items():
        if uri == key:
            data_dict = key
            if key == 'resource_groups':
                data_dict = 'resources'
            data_file = f'{os.path.dirname(__file__)}/{value}/{key}.json'
            with open(data_file, 'r') as json_file:
                try:
                    if is_uuid or is_id:
                        return {'data': json.load(json_file)[data_dict][index]}
                    return {'data': json.load(json_file)}
                except json.JSONDecodeError as err:
                    return err

    return {'error': 'unable to read data'}

def qw(arg1, arg2, path, headers=None, payload=None):
    """This function is used to mock the query_wrapper function from
    utils/common. It returns information collected from get_all()
    function.
    """
    return get_all(path)

def qw_not_found(arg1, arg2, path=None, headers=None, payload=None):
    """This function is used when a not found resource should be returned.
    According arg2 argument, if "not_found" is detected as a string then
    payload is returned directly or as part of "data" dictionnary.
    """
    payload = {'errors': [{
                  'code': 'not_found',
                  'message': 'Resource not found'
                  }]
              }
    if arg2 == 'not_found':
        return payload
    return  {'data': payload}

def qw_api_error(arg1, arg2, path, headers=None, payload=None):
    """This function is used when an unpredicatble error shoudl be returned
    as if something went wrong with the API call. None of the arguments will
    be used.
    """
    return  {'data': {
                'errors': [{
                    'code': 'unpredictable_error',
                    'message': 'API call not performed as expected'
                }]
            }}

def qw_exception(arg1, arg2, path, headers=None, payload=None):
    """This function is used when an exception should be raised. None of the
    arguments will be used.
    """
    raise Exception

def qw_delete_code_204(arg1, arg2, path, headers=None, payload=None):
    """This function is used when a code 204 is required during a resource
    deleting. Using the SimpleNamespace() will help to create an object that
    will contains status as part of the dict. None of the arguments will be
    used. SimpleNamespace() explaination: https://bit.ly/3ylloVs
    """
    response = SimpleNamespace()
    response.status = 204
    return {'response': response}

def qw_delete_code_400(arg1, arg2, path, headers=None, payload=None):
    """This function is used when a code 400 is required during a resource
    deleting to simulate an issue. Using the SimpleNamespace() will help to
    create an object that will contains status as part of the dict. None of
    the arguments will be used. SimpleNamespace() explaination:
    https://bit.ly/3ylloVs
    """
    response = SimpleNamespace()
    response.status = 400
    return {'response': response, 'data': 'bad_request'}
