import os.path
import json
import re


class Return202(object):
    status = 202


class Return204(object):
    status = 204


class Return404(object):
    status = 404


class Common(object):

    resource_path = "tests/resources"

    @classmethod
    def authentication(self, auth_url, key):
        """ Return a false header required by authentication process """
        return {'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization':
                'Bearer eyJraWQiOiIyMDIwMDMyNjE4MjgiLCJhbGciOiJSUzI1NiJ9.e'}

    # @classmethod
    def set_folder(path):
        """
        Set folder variable based on path
        """
        paths = ['vpcs', 'vpn_gateways', 'instances', 'images',
                 'public_gateways', 'keys', 'regions', 'zones',
                 'resource_groups', 'floating_ips', 'resource_instances',
                 'operating_systems', 'subnets']
        for p in paths:
            if p in path:
                folder = p
        return folder

    # @classmethod
    def get_json_resource_content(path):
        folder = Common.set_folder(path)

        try:
            resource_file = os.path.normpath(
                'tests/resources/{}/{}.json').format(folder, folder
            )
            json_file = open(resource_file, mode='rb')
            json_content = json.load(json_file)
            return(json_content)
        except IOError:
            return {"error": "test data file not found"}

    def open_and_load_json_file(full_path):
        resource_file = os.path.normpath(full_path)
        try:
            json_file = open(resource_file, mode='rb')
            json_content = json.load(json_file)
            return(json_content)
        except IOError:
            return {"error": "test data file not found"}

    def return_exception(service, verb, path, headers):
        """
        Will raise an exception
        """
        raise Exception

    def return_exception_5_args(service, verb, path, headers, payload):
        """
        Will raise an exception
        """
        raise Exception

    def return_not_found(service, verb, path, headers):
        """
        Will return an not_found error
        """
        result = {}
        result['data'] = {
            "errors": [
             {
                "code": "not_found",
                "message": "Resource not found"
             }
            ]
        }
        return(result)

    def return_not_found_3_args(service, verb, path):
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

    def return_not_found_5_args(service, verb, path, headers,
                                payload):
        """
        Will return a "not_found" error
        """
        result = {}
        result['data'] = {
            "errors": [
             {
                "code": "not_found",
                "message": "Resource not found"
             }
            ]
        }
        return(result)

    @classmethod
    def return_not_found_2_args(self, service, verb):
        """
        Will return an not_found error
        """
        result = {}
        result['data'] = {
            "errors": [
             {
                "code": "not_found",
                "message": "Resource not found"
             }
            ]
        }
        return(result)

    @classmethod
    def return_error(self, data):
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

    def return_error_1_args(data):
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

    def return_error_3_args(data, verb, header):
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

    def qw(service, verb, path, headers, payload=False):
        """
        This function will replace the original qw function.
        """
        result = {}

        uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}" # noqa

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        if verb == "GET":
            get_one = re.findall('.'+folder+'/'+uuid_regexp, path)

            # we want all the data: if the uuid regexp doesn't match but if we
            # pass a string we should return a  "not_found" error.
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

    def qw_with_payload(service, verb, path, headers, payload):
        return(Common.qw(service, verb, path, headers))

    @classmethod
    def qw_404_on_delete(self, service, verb, path, headers):
        """
        This function will replace the qw and will return 404.
        """

        result = {}

        uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}" # noqa
        folder = self.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        get_one = re.findall('.'+folder+'/'+uuid_regexp, path)

        # we want all the data: if the uuid regexp doesn't match but if we
        # pass a string we should return a  "not_found" error.
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
        if verb == "DELETE":
            result["data"] = "Forbiden"
            result["response"] = Return404()
            return(result)

        # uuid = re.findall(uuid_regexp, path)[0]
        result["data"] = json_content[folder][0]
        return(result)

    @classmethod
    def create(self, service, verb, path, headers, payload):
        """
        This function will simulate API response
        """
        result = {}

        folder = self.set_folder(path)

        json_content = self.get_json_resource_content(path)

        if service == "iaas" and verb == "POST":
            result["data"] = json_content[folder][0]
            return(result)

    # @classmethod
    def get_resource_group(path):
        """
        This function will get resource group name, href and id from the first
        resource record.
        """
        result = {}

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        name = json_content[folder][0]["resource_group"]["name"]
        href = json_content[folder][0]["resource_group"]["href"]
        id = json_content[folder][0]["resource_group"]["id"]

        result = {"data": {
            "href": href,
            "id": id,
            "name": name
            }
        }
        return(result)

    def get_floating_ip(path):
        """
        This function will get resource group name, href and id from the first
        resource record.
        """
        result = {}

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        name = json_content[folder][0]["floating_ip"]["name"]
        href = json_content[folder][0]["floating_ip"]["href"]
        id = json_content[folder][0]["floating_ip"]["id"]
        address = json_content[folder][0]["floating_ip"]["address"]

        result = {"data": {
            "href": href,
            "id": id,
            "name": name,
            "address": address
            }
        }
        return(result)

    def get_vpc(path):
        """
        This function will get resource group name, href and id from the first
        resource record.
        """
        result = {}

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        name = json_content[folder][0]["vpc"]["name"]
        href = json_content[folder][0]["vpc"]["href"]
        id = json_content[folder][0]["vpc"]["id"]

        result = {"data": {
            "href": href,
            "id": id,
            "name": name,
            }
        }
        return(result)

    def get_subnet(path):
        """
        This function will get resource group name, href and id from the first
        resource record.
        """
        result = {}

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        name = json_content[folder][0]["subnet"]["name"]
        href = json_content[folder][0]["subnet"]["href"]
        id = json_content[folder][0]["subnet"]["id"]

        result = {"data": {
            "href": href,
            "id": id,
            "name": name
            }
        }
        return(result)


    @classmethod
    def get_volume(self, resource):
        """
        Return volume information
        """
        result = {"data": {
            "href": "https://us-south.iaas.cloud.ibm.com/v1/volumes/ccbe6fe1-5680-4865-94d3-687076a38293", # noqa
            "id": "cbe6fe1-5680-4865-94d3-687076a38293",
            "name": "my-volume-1",
            }
        }
        return(result["data"])

    @classmethod
    def return_204(self, service, verb, path, headers):
        """
        Return 204
        """
        result = {"data": {
            "response": {
                "status": 204
            }
        }}
        return(result)


class Vpc(Common):
    # try:
    #     resource_file = os.path.normpath('tests/resources/public_gateways/public_gateways.json') # noqa
    #     json_file = open(resource_file, mode='rb')
    #     json_content = json.load(json_file)
    # except IOError:
    #     print("public gateways json file not found")

    # name = "my-vpc-1"
    # id = "882a7764-5f0e-43b5-b276-0d1c39189488"
    pass

