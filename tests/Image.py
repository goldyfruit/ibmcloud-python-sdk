import re

from tests.Common import Common
from tests.Common import Return202


class Image(Common):
    path = "images"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    href = json_content[path][0]["href"]
    id = json_content[path][0]["id"]

    @classmethod
    def return_not_found(self, image):
        service, verb, path, headers = "null", "null", "null", "null"
        result = Common.return_not_found(service, verb, path, headers)
        return(result["data"])

    def return_exception(image):
        """
        Will raise an exception
        """
        raise Exception

    def get_resource_group(self, pgw):
        result = Common.get_resource_group("images")
        return(result["data"])

    def qw_with_payload_return_exception(self, service, verb, path, headers,
                                         payload):
        """
        Will raise an exception
        """
        raise Exception

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
            result["response"] = Return202()
            return(result)

        if verb == "POST":
            result["data"] = json_content[folder][0]
            return(result)


class OperatingSystem(Common):
    path = "operating_systems"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    href = json_content[path][0]["href"]
    vendor = json_content[path][0]["vendor"]

    def qw(service, verb, path, headers):
        """
        Special qw function to handle Operation Systems uniqueness.
        """
        result = {}

        folder = Common.set_folder(path)
        json_content = Common.get_json_resource_content(path)

        regexp = "([a-z0-9-]*)"

        if verb == "GET":
            get_one = re.findall('.'+folder+'/'+regexp, path)

            # we want all the data: if the region regexp doesn't match but if we pass a string
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
