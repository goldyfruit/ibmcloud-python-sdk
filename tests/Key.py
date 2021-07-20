from os import CLD_CONTINUED
import os.path
import json
import re

from tests.Common import Common

class Key(Common):
    path = "keys"

    json_content = Common.get_json_resource_content("keys")

    name = json_content[path][0]["name"]
    id = json_content[path][0]["id"]
    href = json_content[path][0]["href"]

    @classmethod
    def return_not_found(self):
        """
        Will return an not_found error
        """
        result = {}
        result = {
            "errors": [
             {
                "code": "not_found",
                "message": "Resource not found"
             }
            ]
        }
        return(result)

    @classmethod
    def get_resource_group(self, service, verb, path, headers):
        result = {}
        result["data"] = { "resources": [ {
            "id": "fee82deba12e4c0fb69c3b09d1f12345",
            "name": "my-resource-group"
            }
        ]}
        return result

    @classmethod
    def get_keys_return_error(self):
        """
        Will return an error (simulate API errors)
        """
        result = {}
        result = {
            "errors": [{
                "code": "unpredictable_error",
                "message": "Resource has disappeared"
            }]
        }
        return(result)

    @classmethod
    def qw_return_error(self, service, verb, path, headers):
        """
        Will return an error (simulate API errors)
        """
        result = {}
        result["data"] = {
            "errors": [{
                "code": "unpredictable_error",
                "message": "Resource has disappeared"
            }]
        }
        return(result)