import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Vpc():

    def __init__(self):
        self.cfg = params()

    # Get all VPCs
    def get_vpcs(self):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

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
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching VPC with ID {id}. {error}")
            raise

    # Get specific VPC by name
    def get_vpc_by_name(self, name):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve vpc data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over vpc until filter match
            for vpc in data['vpcs']:
                if vpc["name"] == name:
                    # Return data
                    return vpc

            # Return error if no VPC is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching VPC with name {name}. {error}")
            raise

    # Get VPC default network ACL
    def get_vpc_default_network_acl(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_network_acl?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching default network ACL for VPC"
                  " with ID {}. {}").format(id, error)
            raise

    # Get VPC default security group
    def get_vpc_default_security_group(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_security_group?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

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
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return self.common.query_wrapper(
                "iaas", "POST", path, self.headers,
                json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating VPC. {error}")
            raise

    # Delete vpc
    # This method is generic and should be used as prefered choice
    def delete_vpc(self, vpc):
        by_name = self.delete_vpc_by_name(vpc)
        if "errors" in by_name:
            for key_vpc in by_name["errors"]:
                if key_vpc["code"] == "not_found":
                    by_id = self.delete_vpc_by_id(vpc)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete VPC by ID
    def delete_vpc_by_id(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
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
                vpc["id"], self.cfg["version"], self.cfg["generation"])

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting VPC with name {name}. {error}")
            raise
