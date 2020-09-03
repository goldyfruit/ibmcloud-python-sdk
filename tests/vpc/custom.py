import os.path
import json


def fake_get_vpc(self, vpc):
    """
    Return a false header required by authentication process
    """
    result = {}
    resource_file = os.path.normpath('tests/resources/vpcs/vpcs.json')
    # Must return a file-like object
    try:
        json_file = open(resource_file, mode='rb')
        result = json.load(json_file)
        return(result)
    except IOError:
        result["data"] = {"error": "not found"}
        return result
        raise
