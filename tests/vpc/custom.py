import os.path
import requests
import re
import json

from urllib.parse import urlparse

def fake_get_vpc(self, vpc):
    """
    Return a false header required by authentication process
    """
    result = {}
    folder = 'vpcs'
    resource_file = os.path.normpath('tests/resources/vpcs/vpcs.json')
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result = json.load(json_file)
        return(result)
    except IOError:
        print("in da house")
        result["data"] = {"error": "not found"}
        return result
        raise


