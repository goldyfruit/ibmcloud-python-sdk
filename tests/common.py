import os.path
import requests
import re
import json

from urllib.parse import urlparse

def fake_auth(auth_url, key):
    """
    Return a false header required by authentication process
    """
    return {'Content-Type': 'application/json', 'Accept': 'application/json', 
            'Authorization': 'Bearer eyJraWQiOiIyMDIwMDMyNjE4MjgiLCJhbGciOiJ\
                    SUzI1NiJ9.e'}

def fake_get_call(service, verb, path, headers):
    """
    This function will replace the original API.
    """
    result = {}
    result["data"] = {}
   
    if 'vpcs' in path:
        folder = 'vpcs'
    if 'instances' in path:
        folder = 'instances'
    result["data"][folder] = []
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    print(resource_file)
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result["data"][folder].append(json.load(json_file))
        return(result)
    except IOError:
        print("in da house")
        return result["data"]["vpcs"].append({"error": "not found"})
        raise 

def fake_get_one(service, verb, path, headers):
    """
    This function will replace the original API.
    """
    result = {}
    
    if 'vpcs' in path:
        folder = 'vpcs'
    if 'instances' in path:
        folder = 'instances'
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result["data"] = json.load(json_file)
        return(result)
    except IOError:
        return["data"]["vpcs"].append({"error": "not found"})
        raise


