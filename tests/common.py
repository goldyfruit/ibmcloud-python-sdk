import os.path
import json

# from urllib.parse import urlparse


def set_folder_var(path):
    """
    Set folder variable based on path
    """
    if 'vpc' in path:
        folder = 'vpcs'
    if 'vpn' in path:
        folder = 'vpns'
    if 'instances' in path:
        folder = 'instances'
    if 'images' in path:
        folder = 'images'
    if 'public_gateway' in path:
        folder = 'gateways'
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
    return {'Content-Type': 'application/json',
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
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(
        folder,
        folder
    )
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
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(
        folder,
        folder
    )
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
    # folder = set_folder_var(path)
    if service == "iaas" and verb == "POST":
        data = {"id": "r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82",
                "crn": "crn:v1:bluemix:public:is:us-south:a/2d171b8a90\
                 e246fd9ffe0e5e8c191c9e::instance:r006-74ff2772-9f3a-4263\
                -bcaa-12fcffa3ed82",
                "href": "https://us-south.iaas.cloud.ibm.com/v1/instances\
                        /r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82",
                "name": "sdk",
                "status": "available"
                }
        return({"status_code": 200, "data": data})
    else:
        data = {"id": "", "name": "", "status": "error !"}
        return({"status_code": 500, "data": data})


def query_specified_object(path):
    # result = {}
    folder = set_folder_var(path)
    resource_file = os.path.normpath('tests/resources/{}/{}.json').format(
        folder,
        folder
    )
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result = json.load(json_file)
        return(result)
    except IOError:
        return["data"]["vpcs"].append({"error": "not found"})
        raise


def fake_get_vpc(fake, data):
    """
    This function will replace the original API.
    """
    result = query_specified_object('vpc')
    return(result)


def fake_get_resource_group(fake, data):
    """
    This function will replace the original API.
    """
    result = query_specified_object('resource_group')
    return(result)


def fake_get_image(fake, data):
    """
    This function will replace the original API.
    """
    result = query_specified_object('image')
    return(result)


def fake_get_vpn(fake, data):
    """
    This function will replace the original API.
    """
    result = query_specified_object('vpn')
    return(result)


def fake_get_floating_ip(fake, data):
    """
    This function will replace the original API.
    """
    result = query_specified_object('floating_ips')
    return(result)
