from tests.Common import Common


class Subnet(Common):
    path = "subnets"

    json_content = Common.get_json_resource_content(path)

    name = json_content[path][0]["name"]
    id = json_content[path][0]["id"]
    href = json_content[path][0]["href"]

    @classmethod
    def subnet_return_not_found(self):
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
