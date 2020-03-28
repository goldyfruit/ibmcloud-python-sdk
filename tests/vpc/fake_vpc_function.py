import os.path
import requests
import re
import json

from urllib.parse import urlparse

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

