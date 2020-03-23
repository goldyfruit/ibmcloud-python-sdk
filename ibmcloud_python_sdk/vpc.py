import json
from . import config as ic


class Vpc():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn = self.cfg.conn

    # Get all VPC
    def get_vpcs(self):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching VPC. {error}")
            raise

    # Get specific VPC by ID or by name
    # This method is generic and should be used as prefered choice
    def get_vpc(self, vpc):
        by_name = self.get_vpc_by_name(vpc)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_vpc_by_id(vpc)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific VPC by ID
    def get_vpc_by_id(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching VPC with ID {id}. {error}")
            raise

    # Get specific VPC by name
    def get_vpc_by_name(self, name):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Loop over vpc until filter match
            for vpc in json.loads(data)['vpcs']:
                if vpc['name'] == name:
                    # Return response data
                    return vpc

            # Return response if no VPC is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching VPC with name {name}. {error}")
            raise

    # Get VPC default network ACL
    def get_vpc_default_network_acl(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_network_acl?version={}"
                    "&generation={}").format(id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print("Error fetching default network ACL for VPC"
                  " with ID {}. {}").format(id, error)
            raise

    # Get VPC default security group
    def get_vpc_default_security_group(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_security_group?version={}"
                    "&generation={}").format(id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print("Error fetching default security group for VPC"
                  "with id {id}. {error}").format(id, error)
            raise

    # Create VPC
    def create_vpc(self, **kwargs):
        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'address_prefix_management': kwargs.get('addr_mgmt', 'auto'),
            'classic_access': kwargs.get('classic_access', False),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("POST", path, json.dumps(payload), self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error creating VPC. {error}")
            raise

    # Delete VPC by ID
    def delete_vpc_by_id(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("DELETE", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            if res.status != 204:
                return json.loads(data)

            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting VPC with id {id}. {error}")
            raise

    # Delete VPC by name
    def delete_vpc_by_name(self, name):
        try:
            # Check if VPC exists
            vpc = self.get_vpc_by_name(name)
            if "errors" in vpc:
                return vpc

            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                vpc["id"], self.ver, self.gen)
            self.conn.request("DELETE", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            if res.status != 204:
                return json.loads(data)

            # Print and return response data
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting VPC with name {name}. {error}")
            raise
