from tests.Common import Common


class Subnet(Common):
    path = "subnets"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    id = json_content[path][0]["id"]
    href = json_content[path][0]["href"]
    resource_group_id = json_content[path][0]["resource_group"]["id"]
    network_acl= json_content[path][0]["network_acl"]["name"]
    routing_table= json_content[path][0]["routing_table"]["name"]


    def get_vpc(self, subnet):
        result = Common.get_vpc("subnets")
        return(result["data"])

    def get_resource_group(self, subnet):
        result = Common.get_resource_group("subnets")
        return(result["data"])

    def get_network_acl(self, subnet):
        result = Common.get_json_resource_content("subnets")
        return(result["subnets"][0]["network_acl"])

    def subnet_return_not_found(self, service):
        """
        Will return an not_found error
        """
        result = {
            "errors": [
             {
                "code": "not_found",
                "message": "Resource not found"
             }
            ]
        }
        return(result)
