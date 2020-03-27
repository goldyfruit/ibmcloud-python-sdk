import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import gateway as gw


class Subnet():

    def __init__(self):
        self.cfg = params()
        self.gateway = gw.Gateway()

    # Get all subnets
    def get_subnets(self):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching subnets. {error}")
            raise

    # Get specific subnet by ID or by name
    # This method is generic and should be used as prefered choice
    def get_subnet(self, subnet):
        by_name = self.get_subnet_by_name(subnet)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_subnet_by_id(subnet)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific subnet by ID
    def get_subnet_by_id(self, id):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching subnet with ID {id}. {error}")
            raise

    # Get specific subnet by name
    def get_subnet_by_name(self, name):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve subnets data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over subnets until filter match
            for subnet in data["subnets"]:
                if subnet["name"] == name:
                    # Return data
                    return subnet

            # Return error if no subnet is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching subnet with name {name}. {error}")
            raise

    # Get subnet's network ACL by ID or by name
    # This method is generic and should be used as prefered choice
    def get_subnet_network_acl(self, subnet):
        by_name = self.get_subnet_network_acl_by_name(subnet)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_subnet_network_acl_by_id(subnet)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific subnet's network ACL by ID
    def get_subnet_network_acl_by_id(self, id):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/network_acl?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching subnet's network ACL with ID {id}. {error}")
            raise

    # Get specific subnet's network ACL by name
    def get_subnet_network_acl_by_name(self, name):
        try:
            # Retrieve subnet information by name to get the ID
            subnet = self.get_subnet_by_name(name)

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/network_acl?version={}"
                    "&generation={}").format(subnet["id"], self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching subnet's network acl with"
                  "name {}. {}").format(name, error)
            raise

    # Get subnet's public gateway by ID or by name
    # This method is generic and should be used as prefered choice
    def get_subnet_public_gateway(self, subnet):
        by_name = self.get_subnet_public_gateway_by_name(subnet)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_subnet_public_gateway_by_id(subnet)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific subnet's public gateway by ID
    def get_subnet_public_gateway_by_id(self, id):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching subnet's public gateway with"
                  "ID {}. {}").format(id, error)
            raise

    # Get specific subnet's public gateway by name
    def get_subnet_public_gateway_by_name(self, name):
        try:
            # Retrieve subnet information by name to get the ID
            subnet = self.get_subnet_by_name(name)

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}").format(subnet["id"], self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching subnet's public gateway with"
                  "name {}. {}").format(name, error)
            raise

    # Create subnet
    def create_subnet(self, **kwargs):
        # Required parameters
        required_args = set(["vpc", "zone", "total_ipv4_address_count"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'ipv4_cidr_block': kwargs.get('ipv4_cidr_block'),
            'vpc': kwargs.get('vpc'),
            'zone': kwargs.get('zone'),
            'ip_version': kwargs.get('ip_version', 'ipv4'),
            'network_acl': kwargs.get('network_acl'),
            'public_gateway': kwargs.get('public_gateway'),
            'total_ipv4_address_count': kwargs.get('total_ipv4_address_count'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "network_acl":
                if value is not None:
                    payload["network_acl"] = {"id": args["network_acl"]}
            elif key == "public_gateway":
                if value is not None:
                    payload["public_gateway"] = {"id": args["public_gateway"]}
            elif key == "vpc":
                payload["vpc"] = {"id": args["vpc"]}
            elif key == "zone":
                payload["zone"] = {"name": args["zone"]}
            elif key == "ipv4_cidr_block":
                if value is not None:
                    payload["ipv4_cidr_block"] = args["ipv4_cidr_block"]
            elif key == "total_ipv4_address_count":
                payload["total_ipv4_address_count"] = args[
                    "total_ipv4_address_count"]
            else:
                payload[key] = value
        print(payload)
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating subnet. {error}")
            raise

    # Attach network ACL to subnet
    def attach_network_acl(self, **kwargs):
        # Required parameters
        required_args = set(["subnet", "network_acl"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'subnet': kwargs.get('subnet'),
            'network_acl': kwargs.get('network_acl'),
        }

        # Retrieve subnet and network ACL information to get the ID
        # (mostly useful if a name is provided)
        subnet = self.get_subnet(args["subnet"])
        acl = self.get_subnet_network_acl(args["network_acl"])

        # Construct payload
        payload = {}
        payload["id"] = acl["id"]

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/network_acl?version={}"
                    "&generation={}").format(subnet["id"], self.ver,
                                             self.gen)

            # Return data
            return qw("iaas", "PUT", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error attaching network ACL {} to subnet"
                  "{}. {}").format(args["network_acl"], args["subnet"],
                                   error)
            raise

    # Attach public gateway to subnet
    def attach_public_gateway(self, **kwargs):
        # Required parameters
        required_args = set(["subnet", "public_gateway"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'subnet': kwargs.get('subnet'),
            'public_gateway': kwargs.get('public_gateway'),
        }

        # Retrieve subnet and public gateway information to get the ID
        # (mostly useful if a name is provided)
        subnet = self.get_subnet(args["subnet"])
        gateway = self.gateway.get_public_gateway(args["public_gateway"])

        # Construct payload
        payload = {}
        payload["id"] = gateway["id"]

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}").format(subnet["id"], self.ver,
                                             self.gen)

            # Return data
            return qw("iaas", "PUT", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error attaching public gateway with ID {} to subnet with"
                  "ID {}. {}").format(args["public_gateway"], args["subnet"],
                                      error)
            raise

    # Detach subnet'public gateway
    def detach_public_gateway(self, subnet):
        # Retrieve subnet information to get the ID (mostly useful if a name
        # is provided)
        subnet = self.get_subnet(subnet)

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}").format(subnet["id"], self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error detaching subnet's public gateway for"
                  "subnet {}. {}").format(subnet, error)
            raise

    # Delete subnet
    # This method is generic and should be used as prefered choice
    def delete_subnet(self, subnet):
        by_name = self.delete_subnet_by_name(subnet)
        if "errors" in by_name:
            for key_subnet in by_name["errors"]:
                if key_subnet["code"] == "not_found":
                    by_id = self.delete_subnet_by_id(subnet)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete subnet
    def delete_subnet_by_id(self, id):
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting subnet with ID {id}. {error}")
            raise

    # Delete subnet by name
    def delete_subnet_by_name(self, name):
        try:
            # Check if subnet exists
            subnet = self.get_subnet_by_name(name)
            if "errors" in subnet:
                return subnet

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}?version={}&generation={}").format(
                subnet["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting subnet with name {name}. {error}")
            raise
