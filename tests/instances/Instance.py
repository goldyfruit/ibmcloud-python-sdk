
import re
import os
import json

from tests.Common import Common
from tests.Common import Return204


class Instance(Common):
    json_content = Common.get_json_resource_content("instances")

    name = json_content["instances"][0]["name"]
    id = json_content["instances"][0]["id"]

    network_interfaces = json_content["instances"][0]["network_interfaces"]

    network_interface = Common.open_and_load_json_file(
        Common.resource_path+'/instances/network_interfaces.json')
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
            Common.resource_path+'/instances/network_interfaces.json')
        return(result)

    @classmethod
    def get_instance_interfaces(self, instance_id):
        result = {}
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/instances.json')
        return(result["instances"][0])

    @classmethod
    def get_instances(self, instance, verb, path, headers):
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/instances.json')
        return(result["instances"])

    @classmethod
    def get_instance(self, instance):
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/instances.json')
        return(result["instances"][0])

    @classmethod
    def get_instance_with_5_args(self, instance, verb, path, headers):
        result = {}
        result["data"] = {}
        instances = Common.open_and_load_json_file(
            Common.resource_path+'/instances/instances.json')
        result["data"]["instances"] = instances["instances"]
        print(result["data"])
        return(result)

    @classmethod
    def get_instance_interface_by_id(self, instance, interface):
        result = Common.open_and_load_json_file(
            Common.resource_path+'/instances/network_interfaces.json')
        return(result)

    def get_json_resource_content(file):
        folder = Common.set_folder(file)

        try:
            resource_file = os.path.normpath(
                'tests/resources/instances/{}.json').format(folder, folder)
            json_file = open(resource_file, mode='rb')
            json_content = json.load(json_file)
            return(json_content)
        except IOError:
            return {"error": "test data file not found"}

    def set_folder(path):
        """
        Set folder variable based on path
        """
        paths = ['profiles', 'templates', 'disks', 'volume_attachments']
        for p in paths:
            if p in path:
                folder = p
            else:
                folder = 'instances'
        return folder

    def qw(service, verb, path, headers):
        """
        This function will replace the original qw function.
        """
        result = {}

        uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}" # noqa
        # uuid_regexp = "^[-0-9a-z_]"

        folder = Instance.set_folder(path)

        json_content = Instance.get_json_resource_content(path)

        if verb == "GET":
            get_one = re.findall('.'+folder+'/'+uuid_regexp, path)

            # we want all the data: if the uuid regexp doesn't match but if we
            # pass a string we should return a "not_found" error.
            if get_one == []:
                return_error = re.findall('.'+folder+'/', path)
                if return_error == []:
                    result["data"] = json_content
                    return(result)

                if return_error != []:
                    result['data'] = {
                        "errors": [{
                            "code": "not_found",
                            "message": "Resource not found"
                        }]
                    }
                    return(result)
            # we want one record, that one matches the uuid
            # uuid = re.findall(uuid_regexp, path)[0]
            result["data"] = json_content[folder][0]
            return(result)

        if verb == "DELETE":
            result["response"] = Return204()
            return(result)

        if verb == "POST":
            result["data"] = json_content[folder][0]
            return(result)
