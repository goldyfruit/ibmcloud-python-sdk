import os.path
import json
import re

from tests.Common import Common

class Instance(Common):
    json_content = Common.get_json_resource_content("instances")

    name = json_content["instances"][0]["name"]
    id = json_content["instances"][0]["id"]

    network_interfaces = json_content["instances"][0]["network_interfaces"]

    network_interface = Common.open_and_load_json_file(
        Common.resource_path+'/instances/network_interface.json')
    network_interface_name = network_interface["name"]

    @classmethod
    def return_not_found(self, service):
        """
        Will return an not_found error
        """
        # result = {}
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
    def get_instance_interfaces_by_id(self, id):
        result = {}
        result["data"] = self.network_interfaces

    @classmethod
    def get_instance_interfaces_by_name(self, name):
        result = {}
        result["data"] = self.network_interfaces

    @classmethod
    def get_instance_interface_by_name(self, instance, interface):
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/network_interface.json')
        return(result)

    @classmethod
    def get_instance_interface_by_id(self, instance, interface):
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/network_interface.json')
        return(result)