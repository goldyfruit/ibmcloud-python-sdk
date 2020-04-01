import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Vpc():

    def __init__(self):
        self.cfg = params()

    def get_vpcs(self):
        """
        Retrieve VPC list
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching VPC. {error}")
            raise

    def get_vpc(self, vpc):
        """
        Retrieve specific VPC by name or by ID
        :param vpc: VPC name or ID
        """
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

    def get_vpc_by_id(self, id):
        """
        Retrieve specific VPC by ID
        :param id: VPC ID
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching VPC with ID {id}. {error}")
            raise

    def get_vpc_by_name(self, name):
        """
        Retrieve specific VPC by name
        :param id: VPC name
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve vpc data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over VPCs until filter match
            for vpc in data['vpcs']:
                if vpc["name"] == name:
                    # Return data
                    return vpc

            # Return error if no VPC is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching VPC with name {name}. {error}")
            raise

    def get_default_network_acl(self, vpc):
        """
        Retrieve VPC's default network ACL
        :param vpc: VPC name or ID
        """
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

    def get_default_security_group(self, vpc):
        """
        Retrieve VPC's default security group
        :param vpc: VPC name or ID
        """
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
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating VPC. {error}")
            raise

    def delete_vpc(self, vpc):
        """
        Delete VPC
        :param vpc: VPC name or ID
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Check if VPC exists
            vpc = self.get_vpc_by_name(name)
            if "errors" in vpc:
                return vpc

            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}").format(
                vpc["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting VPC with name {name}. {error}")
            raise
