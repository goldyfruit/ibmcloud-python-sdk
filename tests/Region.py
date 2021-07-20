from os import CLD_CONTINUED
import os.path
import json
import re

from tests.Common import Common

class Region(Common):

    path = "regions"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    href = json_content[path][0]["href"]

    def qw(service, verb, path, headers):
        """
        Special qw function to handle RegionZone uniqueness.
        """
        result = {}

        folder = Common.set_folder(path)
        json_content = Common.get_json_resource_content(path)

        # regexp = "([a-z]|[a-z][-a-z0-9]*[a-z0-9]|[0-9][-a-z0-9]*([a-z]|[-a-z][-a-z0-9]*[a-z0-9]))$"
        regexp = "([a-z][a-z]-[a-z0-9]*)"

        if verb == "GET":
            get_one = re.findall('.'+folder+'/'+regexp, path)

            # we want all the data: if the region regexp doesn't match but if we pass a string
            # we should return a  "not_found" error.
            if get_one == []:
                return_error = re.findall('.'+folder+'/', path)
                if  return_error == []:
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
