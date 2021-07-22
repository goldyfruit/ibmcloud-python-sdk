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
        paths = ['vpcs', 'vpn_gateways', 'instances', 'images', 'public_gateways',
                 'keys', 'regions', 'zones', 'resource_groups', 'floating_ips',
                 'resource_instances', 'operating_systems']
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


    def qw(service, verb, path, headers):
        """
        This function will replace the original qw function.
        """
        result = {}

        uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

        folder = Common.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        if verb == "GET":
            get_one = re.findall('.'+folder+'/'+uuid_regexp, path)

            # we want all the data: if the uuid regexp doesn't match but if we pass a string
            # we should return a  "not_found" error.
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

        uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
        folder = self.set_folder(path)

        json_content = Common.get_json_resource_content(path)

        get_one = re.findall('.'+folder+'/'+uuid_regexp, path)

        # we want all the data: if the uuid regexp doesn't match but if we pass a string
        # we should return a  "not_found" error.
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

    @classmethod
    def get_volume(self, resource):
        """
        Return volume information
        """
        result = {"data": {
            "href": "https://us-south.iaas.cloud.ibm.com/v1/volumes/ccbe6fe1-5680-4865-94d3-687076a38293",
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
    #     resource_file = os.path.normpath('tests/resources/public_gateways/public_gateways.json')
    #     json_file = open(resource_file, mode='rb')
    #     json_content = json.load(json_file)
    # except IOError:
    #     print("public gateways json file not found")

    # name = "my-vpc-1"
    # id = "882a7764-5f0e-43b5-b276-0d1c39189488"
    pass




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
            'Authorization': 'Bearer eyJraWQiOiIyMDIwMDMyNjE4MjgiLCJhbGciOiJSUzI1NiJ9.e'}


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
        # return result["data"][folder].append({"error": "not found"})
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
        # return["data"]["vpcs"].append({"error": "not found"})
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
        # return["data"]["vpcs"].append({"error": "not found"})
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
