import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.resource import resource_group


class Fip():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.ResourceGroup()

    def get_floating_ips(self):
        """Retrieve floating IP list

        :return: List of floating IPs
        :rtype: list
        """
        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IPs. {}".format(error))
            raise

    def get_floating_ip(self, fip):
        """Retrieve specific floating IP

        :param fip: Floating IP name, ID or address
        :type fip: str
        :return: Floating IP information
        :rtype: dict
        """
        by_name = self.get_floating_ip_by_name(fip)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_floating_ip_by_id(fip)
                    if "errors" in by_id:
                        for key_id in by_id["errors"]:
                            if key_id["code"] == "not_found":
                                by_addr = self.get_floating_ip_by_address(fip)
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

    def get_floating_ip_by_id(self, id):
        """Retrieve specific floating IP by ID

        :param id: Floating IP ID
        :type id: str
        :return: Floating IP information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IP with ID {}. {}".format(
                id, error))
            raise

    def get_floating_ip_by_name(self, name):
        """Retrieve specific floating IP by name

        :param name: Floating IP name
        :type name: str
        :return: Floating IP information
        :rtype: dict
        """
        try:
            # Retrieve floating IPs
            data = self.get_floating_ips()
            if "errors" in data:
                return data

            # Loop over instances until filter match
            for fip in data["floating_ips"]:
                if fip["name"] == name:
                    # Return data
                    return fip

            # Return error if no floating ips is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching floating IP with name {}. {}".format(
                name, error))
            raise

    def get_floating_ip_by_address(self, address):
        """Retrieve specific floating IP by address

        :param address: Floating IP address
        :type address: str
        :return: Floating IP information
        :rtype: dict
        """
        try:
            # Retrieve floating IPs
            data = self.get_floating_ips()
            if "errors" in data:
                return data

            # Loop over instances until filter match
            for fip in data["floating_ips"]:
                if fip["address"] == address:
                    # Return data
                    return fip

            # Return error if no floating ips is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching floating IP with address {}. {}".format(
                address, error))
            raise

    # Reserve floating IP
    def reserve_floating_ip(self, **kwargs):
        """Create floating IP

        :param name: The unique user-defined name for this floating IP
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param target: The target this address is to be bound to
        :type target: str, optional
        :param zone: The identity of the zone to provision a floating IP in
        :type zone: str, optional
        """
        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'target': kwargs.get('target'),
            'resource_group': kwargs.get('resource_group'),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "target":
                    payload["target"] = {"id": args["target"]}
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "zone":
                    payload["zone"] = {"name": args["zone"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error reserving floating. {}".format(error))
            raise

    def release_floating_ip(self, fip):
        """Release floating IP

        :param fip: Floating IP name, ID or address
        :type fip: str
        """
        try:
            # Check if floating IP exists
            fip_info = self.get_floating_ip(fip)
            if "errors" in fip_info:
                return fip_info

            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips/{}?version={}&generation={}".format(
                fip_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting floating IP {}. {}".format(fip, error))
            raise
