import json

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Vpc():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.ResourceGroup()

    def get_vpcs(self):
        """Retrieve VPC list

        :return: List of VPCs
        :rtype: list
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPCs. {}".format(error))
            raise

    def get_vpc(self, vpc):
        """Retrieve specific VPC by name or by ID

        :param vpc: VPC name or ID
        :type vpc: str
        :return: VPC information
        :rtype: dict
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
        """Retrieve specific VPC by ID

        :param id: VPC ID
        :type id: str
        :return: VPC information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPC with ID {}. {}".format(id, error))
            raise

    def get_vpc_by_name(self, name):
        """Retrieve specific VPC by name

        :param name: VPC name
        :type name: str
        :return: VPC information
        :rtype: dict
        """
        try:
            # Retrieve VPCs
            data = self.get_vpcs()
            if "errors" in data:
                return data

            # Loop over VPCs until filter match
            for vpc in data['vpcs']:
                if vpc["name"] == name:
                    # Return data
                    return vpc

            # Return error if no VPC is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching VPC with name {}. {}".format(name, error))
            raise

    def get_default_network_acl(self, vpc):
        """Retrieve VPC's default network ACL

        :param vpc: VPC name or ID
        :type vpc: str
        :return: Default network information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_network_acl?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching default network ACL for VPC"
                  " {}. {}".format(vpc, error))
            raise

    def get_default_security_group(self, vpc):
        """Retrieve VPC's default security group

        :param vpc: VPC name or ID
        :type vpc: str
        :return: Default security group information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/default_security_group?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching default security group for VPC"
                  " {}. {}".format(vpc, error))
            raise

    def get_address_prefixes(self, vpc):
        """Retrieve VPC address pool prefix list

        :param vpc: VPC name or ID
        :type vpc: str
        :return: List of adress prefixes
        :rtype: list
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching address prefixes in VPC {}. {}".format(
                vpc, error))
            raise

    def get_address_prefix(self, vpc, prefix):
        """Retrieve specific VPC address prefix by name or by ID

        :param vpc: VPC name or ID
        :type vpc: str
        :param prefix: Address prefix name or ID
        :type prefix: str
        :return: Address prefix information
        :rtype: dict
        """
        by_name = self.get_address_prefix_by_name(vpc, prefix)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_address_prefix_by_id(vpc, prefix)
                    if "errors" in by_id:
                        for key_id in by_id["errors"]:
                            if key_id["code"] == "not_found":
                                by_addr = self.get_address_prefix_by_cidr(
                                    vpc, prefix)
                                if "errors" in by_addr:
                                    return by_addr
                                else:
                                    return by_addr
                            else:
                                return by_id
                    else:
                        return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_address_prefix_by_id(self, vpc, id):
        """Retrieve specific VPC address prefix by ID

        :param vpc: VPC name or ID
        :type vpc: str
        :param id: Address prefix ID
        :type id: str
        :return: Address prefix information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching address prefix with ID {} in VPC {}."
                  " {}".format(id, vpc, error))
            raise

    def get_address_prefix_by_name(self, vpc, name):
        """Retrieve specific VPC address prefix by name

        :param vpc: VPC name or ID
        :type vpc: str
        :param name: Address prefix name
        :type name: str
        :return: Address prefix information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Retrieve address prefixes
            data = self.get_address_prefixes(vpc_info["id"])
            if "errors" in data:
                return data

            # Loop over address prefixes until filter match
            for prefix in data['address_prefixes']:
                if prefix["name"] == name:
                    # Return data
                    return prefix

            # Return error if no address prefix is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching address prefix with name {} in VPC {}."
                  " {}".format(name, vpc, error))
            raise

    def get_address_prefix_by_cidr(self, vpc, cidr):
        """Retrieve specific VPC address prefix by cidr

        :param vpc: VPC name or ID
        :type vpc: str
        :param cidr: Address prefix CIDR
        :type cidr: str
        :return: Address prefix information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Retrieve address prefixes
            data = self.get_address_prefixes(vpc_info["id"])
            if "errors" in data:
                return data

            # Loop over address prefixes until filter match
            for prefix in data['address_prefixes']:
                if prefix["cidr"] == cidr:
                    # Return data
                    return prefix

            # Return error if no address prefix is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching address prefix with CIDR {} in VPC {}."
                  " {}".format(cidr, vpc, error))
            raise

    def get_routes(self, vpc):
        """Retrieve route list from VPC default routing table

        :param vpc: VPC name or ID
        :type vpc: str
        :return: List of routing tables
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/routes?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching routes from VPC {}. {}".format(
                vpc, error))
            raise

    def get_route(self, vpc, route):
        """Retrieve specific route from VPC default routing table by name or
        by ID

        :param vpc: VPC name or ID
        :type vpc: str
        :param table: Routing table name or ID
        :type table: str
        :return: Routing table information
        :rtype: dict
        """
        by_name = self.get_route_by_name(vpc, route)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_route_by_id(vpc, route)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_route_by_id(self, vpc, id):
        """Retrieve specific route from VPC default routing table by ID

        :param vpc: VPC name or ID
        :type vpc: str
        :param id: Routing table ID
        :type id: str
        :return: Routing table information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/routes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching route with ID {} in VPC {}. {}".format(
                id, vpc, error))
            raise

    def get_route_by_name(self, vpc, name):
        """Retrieve specific route from VPC default routing table by name

        :param vpc: VPC name or ID
        :type vpc: str
        :param name: Routing table name
        :type name: str
        :return: Routing table information
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Retrieve routes
            data = self.get_routes(vpc_info["id"])
            if "errors" in data:
                return data

            # Loop over routes until filter match
            for prefix in data['routes']:
                if prefix["name"] == name:
                    # Return data
                    return prefix

            # Return error if no route is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching route with name {} in VPC {}. {}".format(
                name, vpc, error))
            raise

    def create_vpc(self, **kwargs):
        """Create VPC (Virtual Private Cloud)

        :param name: The unique user-defined name for this VPC
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param address_prefix_management: Indicates whether a default address
            prefix should be automatically created for each zone in this VPC,
            defaults to `auto`
        :type address_prefix_management: str, optional
        :param classic_access: Indicates whether this VPC should be connected
            to Classic Infrastructure, defaults to `False`
        :type classic_access: bool, optional
        """
        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'address_prefix_management': kwargs.get(
                'address_prefix_management', 'auto'),
            'classic_access': kwargs.get('classic_access', False),
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
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating VPC. {}".format(error))
            raise

    def create_address_prefix(self, **kwargs):
        """Create address prefix

        :param vpc: VPC name or ID
        :type vpc: str
        :param name: The user-defined name for this address prefix
        :type name: str, optional
        :param cidr: The CIDR block for this address prefix
        :type cidr: str
        :param is_default: Indicates whether this is the default prefix for
            this zone in this VPC
        :type is_default: bool, optional
        :param zone: The zone this address prefix is to belong to
        :type zone: str
        :return: Address prefix information
        :rtype: dict
        """
        args = ["vpc", "cidr", "zone"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'vpc': kwargs.get('vpc'),
            'name': kwargs.get('name'),
            'cidr': kwargs.get('cidr'),
            'is_default': kwargs.get('is_default', False),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "vpc" and value is not None:
                if key == "zone":
                    payload["zone"] = {"name": args["zone"]}
                else:
                    payload[key] = value

        # Check if VPC exists and get information
        vpc_info = self.get_vpc(args['vpc'])
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating address prefix in VPC {}. {}".format(
                args['vpc'], error))
            raise

    def create_route(self, **kwargs):
        """Create route in VPC default routing table

        :param vpc: VPC name or ID
        :type vpc: str
        :param name: The user-defined name for this route
        :type name: str, optional
        :param destination: The destination of the route
        :type destination: str
        :param next_hop: The next hop that packets will be delivered to
        :type next_hop: str, optional
        :param zone: The zone to apply the route to
        :type zone: str
        :param action: The action to perform with a packet matching the route
        :type action: str
        :return: Route list information
        :rtype: dict
        """
        args = ["vpc", "destination", "zone"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'vpc': kwargs.get('vpc'),
            'name': kwargs.get('name'),
            'destination': kwargs.get('destination'),
            'next_hop': kwargs.get('next_hop'),
            'zone': kwargs.get('zone'),
            'action': kwargs.get('action')
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "vpc" and value is not None:
                if key == "zone":
                    payload["zone"] = {"name": args["zone"]}
                elif key == "next_hop":
                    payload["next_hop"] = {"address": args["next_hop"]}
                else:
                    payload[key] = value

        # Check if VPC exists and get information
        vpc_info = self.get_vpc(args['vpc'])
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/routes?version={}"
                    "&generation={}".format(vpc_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating route in VPC {}. {}".format(
                args['vpc'], error))
            raise

    def delete_vpc(self, vpc):
        """Delete VPC

        :param vpc: VPC name or ID
        :type vpc: str
        :return: Delete status
        :rtype: resource_deleted()
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}?version={}&generation={}".format(
                vpc_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting VPC {}. {}".format(vpc, error))
            raise

    def delete_address_prefix(self, vpc, prefix):
        """Delete address prefix

        :param vpc: VPC name or ID
        :type vpc: str
        :param prefix: Address prefix name or ID
        :type prefix: str
        :return: Delete status
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        # Check if address prefix exists and get information
        prefix_info = self.get_address_prefix(vpc, prefix)
        if "errors" in prefix_info:
            return prefix_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/address_prefixes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], prefix_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting address prefix {} in VPC {}. {}".format(
                prefix, vpc, error))
            raise

    def delete_route(self, vpc, route):
        """Delete route from VPC default routing table

        :param vpc: VPC name or ID
        :type vpc: str
        :param table: Routing table name or ID
        :type table: str
        :return: Delete status
        :rtype: dict
        """
        # Check if VPC exists and get information
        vpc_info = self.get_vpc(vpc)
        if "errors" in vpc_info:
            return vpc_info

        # Check if route exists and get information
        route_info = self.get_route(vpc, route)
        if "errors" in route_info:
            return route_info

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/vpcs/{}/routes/{}?version={}"
                    "&generation={}".format(vpc_info["id"], route_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting route {} from VPC {}. {}".format(
                route, vpc, error))
            raise
