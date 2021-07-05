import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import gateway as gw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.vpc import acl
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Subnet():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.gateway = gw.Gateway()
        self.acl = acl.Acl()
        self.rg = resource_group.ResourceGroup()

    def get_subnets(self):
        """Retrieve subnet list

        :return: List of subnets
        :rtype: list
        """
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching subnets. {}".format(error))
            raise

    def get_subnet(self, subnet):
        """Retrieve specific subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :return: Subnet information
        :rtype: dict
        """
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

    def get_subnet_by_id(self, id):
        """Retrieve specific subnet by ID

        :param id: Subnet ID
        :type id: str
        :return: Subnet information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching subnet with ID {}. {}".format(id, error))
            raise

    def get_subnet_by_name(self, name):
        """Retrieve specific subnet by name

        :param name: Subnet name
        :type name: str
        :return: Subnet information
        :rtype: dict
        """
        try:
            # Retrieve subnets
            data = self.get_subnets()
            if "errors" in data:
                return data

            # Loop over subnets until filter match
            for subnet in data["subnets"]:
                if subnet["name"] == name:
                    # Return data
                    return subnet

            # Return error if no subnet is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching subnet with name {}. {}".format(name, error))
            raise

    def get_subnet_network_acl(self, subnet):
        """Retrieve network ACL for a specific subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :return: Network ACL information
        :rtype: dict
        """
        try:
            # Check if subnet exists and get information
            subnet_info = self.get_subnet(subnet)
            if "errors" in subnet_info:
                return subnet_info

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/network_acl?version={}"
                    "&generation={}".format(subnet_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network ACL for subnet {}. {}".format(
                subnet, error))
            raise

    def get_subnet_public_gateway(self, subnet):
        """Retrieve public gateway for a specific subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :return: Public gateway information
        :rtype: dict
        """
        try:
            # Check if subnet exists and get information
            subnet_info = self.get_subnet(subnet)
            if "errors" in subnet_info:
                return subnet_info

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}".format(subnet_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching public gateway for subnet {}. {}".format(
                subnet, error))
            raise

    def create_subnet(self, **kwargs):
        """Create subnet

        :param name: The unique user-defined name for this subnet
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param ipv4_cidr_block: The IPv4 range of the subnet, expressed in
            CIDR format
        :type ipv4_cidr_block: str
        :param vpc: The VPC the subnet is to be a part of
        :type vpc: str
        :param zone: The zone the subnet is to reside in
        :type zone: str
        :param ip_version: The IP version(s) supported
        :type ip_version: str, optional
        :param network_acl: The network ACL to use for this subnet
        :type network_acl: str, optional
        :param public_gateway: The public gateway to handle internet bound
            traffic for this subnet
        :type public_gateway: str, optional
        :param routing_table: The routing table for this subnet
        :type routing_table: str, optional
        :param total_ipv4_address_count: The total number of IPv4 addresses
            required
        :type total_ipv4_address_count: int, optional
        """
        args = ["vpc"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'ipv4_cidr_block': kwargs.get('ipv4_cidr_block'),
            'vpc': kwargs.get('vpc'),
            'zone': kwargs.get('zone'),
            'ip_version': kwargs.get('ip_version', 'ipv4'),
            'network_acl': kwargs.get('network_acl'),
            'public_gateway': kwargs.get('public_gateway'),
            'routing_table': kwargs.get('routing_table'),
            'total_ipv4_address_count': kwargs.get('total_ipv4_address_count'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "network_acl":
                    acl_info = self.get_subnet_network_acl(args["network_acl"])
                    if "errors" in acl_info:
                        return acl_info
                    payload["network_acl"] = {"id": acl_info["id"]}
                elif key == "public_gateway":
                    gateway_info = self.get_subnet_public_gateway(
                        args["public_gateway"])
                    if "errors" in gateway_info:
                        return gateway_info
                    payload["public_gateway"] = {"id": gateway_info["id"]}
                elif key == "routing_table":
                    payload["routing_table"] = {"id": args["routing_table"]}
                elif key == "vpc":
                    vpc_info = self.vpc.get_vpc(args["vpc"])
                    if "errors" in vpc_info:
                        return vpc_info
                    payload["vpc"] = {"id": vpc_info["id"]}
                elif key == "zone":
                    payload["zone"] = {"name": args["zone"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating subnet. {}".format(error))
            raise

    # Attach network ACL to subnet
    def attach_network_acl(self, **kwargs):
        """Attach network ACL to a subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :param network_acl: Network ACL name or ID
        :type network_acl: str
        """
        args = ["subnet", "network_acl"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'subnet': kwargs.get('subnet'),
            'network_acl': kwargs.get('network_acl'),
        }

        # Retrieve subnet and network ACL information to get the ID
        # (mostly useful if a name is provided)
        subnet_info = self.get_subnet(args["subnet"])
        if "errors" in subnet_info:
            return subnet_info
        acl_info = self.acl.get_network_acl(args["network_acl"])
        if "errors" in acl_info:
            return acl_info

        # Construct payload
        payload = {}
        payload["id"] = acl_info["id"]

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/network_acl?version={}"
                    "&generation={}".format(subnet_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "PUT", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error attaching network ACL {} to subnet"
                  "{}. {}".format(args["network_acl"], args["subnet"],
                                  error))
            raise

    def attach_public_gateway(self, **kwargs):
        """Attach public gateway to a subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :param public_gateway: Public gateway name or ID
        :type public_gateway: str
        """
        args = ["subnet", "public_gateway"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'subnet': kwargs.get('subnet'),
            'public_gateway': kwargs.get('public_gateway'),
        }

        # Retrieve subnet and public gateway information to get the ID
        # (mostly useful if a name is provided)
        subnet_info = self.get_subnet(args["subnet"])
        gateway_info = self.gateway.get_public_gateway(args["public_gateway"])
        if "errors" in subnet_info:
            return subnet_info
        elif "errors" in gateway_info:
            return gateway_info

        # Construct payload
        payload = {}
        payload["id"] = gateway_info["id"]

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}".format(subnet_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "PUT", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error attaching public gateway {} to subnet {}. {}".format(
                args["public_gateway"], args["subnet"], error))
            raise

    def detach_public_gateway(self, subnet):
        """Detach public gateway from a subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :return: Detach status
        :rtype: resource_deleted()
        """
        # Retrieve subnet and public gateway information to get the ID
        # (mostly useful if a name is provided)
        subnet_info = self.get_subnet(subnet)
        if "errors" in subnet_info:
            return subnet_info

        try:
            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}/public_gateway?version={}"
                    "&generation={}".format(subnet_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error detaching subnet's public gateway for"
                  "subnet {}. {}".format(subnet, error))
            raise

    def delete_subnet(self, subnet):
        """Delete subnet

        :param subnet: Subnet name or ID
        :type subnet: str
        :return: Delete status
        :rtype: resource_deleted()
        """
        try:
            # Check if subnet exists
            subnet_info = self.get_subnet(subnet)
            if "errors" in subnet_info:
                return subnet_info

            # Connect to api endpoint for subnets
            path = ("/v1/subnets/{}?version={}&generation={}".format(
                subnet_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting subnet with name {}. {}".format(subnet,
                                                                  error))
            raise
