import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.vpc import floating_ip
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Gateway():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.fip = floating_ip.Fip()
        self.rg = resource_group.ResourceGroup()

    def get_public_gateways(self):
        """Retrieve public gateways list

        :return: List of public gateways
        :rtype: list
        """
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching public gateways. {}".format(error))
            raise

    def get_public_gateway(self, gateway):
        """Retrieve specific public gateway

        :param gateway: Public gateway name or ID
        :type gateway: str
        :return: Public gateway information
        :rtype: dict
        """
        by_name = self.get_public_gateway_by_name(gateway)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_public_gateway_by_id(gateway)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_public_gateway_by_id(self, id):
        """Retrieve specific public gateway by ID

        :param id: Public gateway ID
        :type id: str
        :return: Public gateway information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching public gateway with ID {}. {}".format(
                id, error))
            raise

    def get_public_gateway_by_name(self, name):
        """Retrieve specific public gateway by name

        :param name: Public gateway name
        :type name: str
        :return: Public gateway information
        :rtype: dict
        """
        try:
            # Retrieve public gateways
            data = self.get_public_gateways()
            if "errors" in data:
                return data

            # Loop over gateways until filter match
            for gateway in data["public_gateways"]:
                if gateway["name"] == name:
                    # Return data
                    return gateway

            # Return error if no public gateway is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching public gateway with name {}. {}".format(
                name, error))
            raise

    def create_public_gateway(self, **kwargs):
        """Create public gateway

        :param name: The unique user-defined name for this subnet
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param floating_ip: Identifies a floating IP by a unique property
        :type floating_ip: str, optional
        :param vpc: The VPC the public gateway is to be a part of
        :type vpc: str
        :param zone: The zone the public gateway is to reside in
        :type zone: str
        """
        args = ["vpc", "zone"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'floating_ip': kwargs.get('floating_ip'),
            'vpc': kwargs.get('vpc'),
            'zone': kwargs.get('zone'),
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
                elif key == "floating_ip":
                    fip_info = self.fip.get_floating_ip(args["floating_ip"])
                    if "errors" in fip_info:
                        return fip_info
                    payload["floating_ip"] = {"address": fip_info["address"]}
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
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating public gateway. {}".format(error))
            raise

    def delete_public_gateway(self, gateway):
        """Delete public gateway

        :param gateway: Public gateway name or ID
        :type gateway: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if public gateway exists
            gateway_info = self.get_public_gateway(gateway)
            if "errors" in gateway_info:
                return gateway_info

            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/{}?version={}&generation={}".format(
                gateway_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting public gateway with name {}. {}".format(
                gateway, error))
            raise
