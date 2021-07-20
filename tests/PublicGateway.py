from os import CLD_CONTINUED
import os.path
import json
import re

from tests.Common import Common

class PublicGateway(Common):
    path = "public_gateways"

    json_content = Common.get_json_resource_content("public_gateways")

    name = json_content[path][0]["name"]
    id = json_content[path][0]["id"]
    href = json_content[path][0]["href"]
    resource_group_name = json_content[path][0]["resource_group"]["name"]
    resource_group_id = json_content[path][0]["resource_group"]["id"]

    def get_resource_group(self, pgw):
        result = Common.get_resource_group("public_gateways")
        return(result["data"])

    def get_floating_ip(self, pgw):
        result = Common.get_floating_ip("public_gateways")
        return(result["data"])

    def get_vpc(self, pgw):
        result = Common.get_vpc("public_gateways")
        return(result["data"])

    @classmethod
    def return_not_found(self, service):
        service, verb, path, headers="null","null","null","null"
        result = Common.return_not_found(service, verb, path, headers)
        return(result["data"])

        # path = "public_gateways"
        # folder = Common.set_folder(path)

        # json_content = Common.get_json_resource_content(path)

        # name = json_content[folder][0]["resource_group"]["name"]
        # href = json_content[folder][0]["resource_group"]["href"]
        # id = json_content[folder][0]["resource_group"]["id"]

        # result = {"data": {
        #         "resources": [{
        #             "href": href,
        #             "id": id,
        #             "name": name
        #             }
        #         ]
        #     }
        # }
        # return(result)
