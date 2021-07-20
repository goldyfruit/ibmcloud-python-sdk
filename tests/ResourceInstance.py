import os.path
import json
import re

from tests.Common import Common

class ResourceInstance(Common):
    json_content = Common.get_json_resource_content("resource_instances")

    name = json_content["resources"][0]["name"]
    id = json_content["resources"][0]["id"]

    resource_group_id = json_content["resources"][0]["resource_group_id"]
    resource_plan_id = json_content["resources"][0]["resource_plan_id"]
    target_crn = json_content["resources"][0]["target_crn"]

    @classmethod
    def get_resource_group(self, pgw):
        result = {}
        result["data"] = {"id": self.resource_group_id }
        return(result["data"])

    @classmethod
    def return_exception(self, service, verb, path, headers, payload):
        """
        Will raise an exception
        """
        raise Exception

    @classmethod
    def qw_5_args(self, service, verb, path, headers, payload):
        result = {}

        result["data"] = self.json_content
        return(result)