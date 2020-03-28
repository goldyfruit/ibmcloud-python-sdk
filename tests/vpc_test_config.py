import os.path
import requests
import re
import json

from urllib.parse import urlparse

def fake_auth(auth_url, key):
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
        folder = 'vpc'
        result["data"]["vpcs"] = []
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    # Must return a file-like object
    print(resource_file)
    try:
        json_file = open(resource_file, mode='rb')
        result["data"]["vpcs"].append(json.load(json_file))
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
    
    if 'vpc' in path:
        folder = 'vpc'
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result["data"] = json.load(json_file)
        return(result)
    except IOError:
        return["data"]["vpcs"].append({"error": "not found"})
        raise

def fake_create_vpc(service, verb, path, headers, payload):
    """
    Test
    """
    #r = requests.Response()
    path_pattern = '/v1\/vpcs\?version=[0-9]{4}-[0-9]{2}-[0-9]{2}&generation=[0-9]'
    contain_path = re.compile(path_pattern)
    if service == "iaas" and verb == "POST" and bool(contain_path.search(path)) is True:
        data = {}
        data = { "id": "r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82", "crn": "crn:v1:bluemix:public:is:us-south:a/2d171b8a90e246fd9ffe0e5e8c191c9e::vpc:r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82", "href": "https://us-south.iaas.cloud.ibm.com/v1/vpcs/r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82", "name": "sdk", "status": "available"}
        return({"status_code": 200, "data": data})
    else:
        data = {}
        data = {"id": "", "name": "", "status": "error !"}
        return({"status_code": 500, "data": data})

