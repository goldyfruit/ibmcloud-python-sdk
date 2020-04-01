import os.path
import requests
import re
import json

from urllib.parse import urlparse


def set_folder_var(path):
    """
    Set folder variable based on path
    """
    if 'vpcs' in path:
        folder = 'vpcs'
    if 'instances' in path:
        folder = 'instances'
    if 'images' in path:
        folder = 'images'
    if 'keys' in path:
        folder = 'keys'
    if 'regions' in path:
        folder = 'regions'
    if 'resource_groups' in path:
        folder = 'resource_groups'
    if 'floating_ips' in path:
        folder = 'floating_ips'

    return folder

def fake_auth(auth_url, key):
    """
    Return a false header required by authentication process
    """
    return {'Content-Type': 'application/json', \
            'Accept': 'application/json', 
            'Authorization': 'Bearer eyJraWQiOiIyMDIwMDMyNjE4MjgiLCJhbGciOiJ\
                    SUzI1NiJ9.e'}

def fake_get_call(service, verb, path, headers):
    """
    This function will replace the original API.
    """
    result = {}
    result["data"] = {}
    folder = set_folder_var(path)
    result["data"][folder] = []
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    #print(resource_file)
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result["data"][folder].append(json.load(json_file))
        return(result)
    except IOError:
        print("in da house")
        return result["data"][folder].append({"error": "not found"})
        raise 

def fake_get_one(service, verb, path, headers):
    """
    This function will replace the original API.
    """
    result = {}
    
    folder = set_folder_var(path)
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(folder, folder)
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result["data"] = json.load(json_file)
        return(result)
    except IOError:
        return["data"]["vpcs"].append({"error": "not found"})
        raise


def fake_create(service, verb, path, headers, payload):
    """
    Test
    """
    data = {}
    folder = set_folder_var(path)
    path_pattern = '\/v1\/'+folder+'\?version=[0-9]{4}-[0-9]{2}-[0-9]{2}&generation=[0-9]'
    vpc_acl_or_sg_pattern = '\/v1\/vpcs\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\/default_security_group\?version=[0-9]{4}-[0-9]{2}-[0-9]{2}\&generation=[0-9]{1}'
    contain_path = re.compile(path_pattern)
    contain_acl_or_sg_path = re.compile(vpc_acl_or_sg_pattern)
    #print(path_pattern)
    #print(path)
    print(bool(contain_path.search(path)))
    print(bool(contain_acl_or_sg_path.search(path)))
    if service == "iaas" and verb == "POST" and\
            (bool(contain_path.search(path)) is True or bool(contain_acl_or_sg_path(path)) is True):
        data = { "id": "r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82", \
                "crn": "crn:v1:bluemix:public:is:us-south:a/2d171b8a90e246fd9ffe0e5e8c191c9e:\
                :instance:r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82", \
                "href": "https://us-south.iaas.cloud.ibm.com/v1/instances/r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82",\
                "name": "sdk", \
                "status": "available"}
        return({"status_code": 200, "data": data})
    else:
        data = {"id": "", "name": "", "status": "error !"}
        return({"status_code": 500, "data": data})

