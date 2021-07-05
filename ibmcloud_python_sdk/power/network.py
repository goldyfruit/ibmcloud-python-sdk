import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.power import instance
from ibmcloud_python_sdk.utils.common import check_args


class Network():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_networks(self, instance):
        """Retrieve network list from cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: Network list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks".format(
                ci_info["name"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching Power Virtual Instance list for cloud"
                  " instance {}. {}".format(instance, error))

    def get_network(self, instance, network):
        """Retrieve specific network by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param network: Network name or ID
        :type network: str
        :return: Network information
        :rtype: dict
        """
        by_name = self.get_pvm_by_name(instance, network)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_pvm_by_id(instance, network)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_network_by_id(self, instance, id):
        """Retrieve specific network by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param id: Network ID
        :type id: str
        :return: Network information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks/{}".format(
                ci_info["name"], id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network with ID {} for cloud instance {}."
                  " {}".format(id, instance, error))

    def get_network_by_name(self, instance, name):
        """Retrieve specific network by name

        :param instance: Cloud instance ID
        :type instance: str
        :param name: Network name
        :type name: str
        :return: Network information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Retrieve networks
            data = self.get_networks(ci_info["name"])
            if "errors" in data:
                return data

            # Loop over networks until filter match
            for network in data['networks']:
                if network["name"] == name:
                    # Return data
                    return network

            # Return error if no network is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching network with name {} for cloud instance {}."
                  " {}".format(name, instance, error))

    def get_ports(self, instance, network):
        """Retrieve port list from from network

        :param instance: Cloud instance ID
        :type instance: str
        :param network: Network name or ID
        :type netowkr: str
        :return: Port list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if network exists and retrieve information
            net_info = self.get_network(ci_info["name"], network)
            if "errors" in net_info:
                return net_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks/{}/ports".format(
                ci_info["name"], net_info["networkID"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching port list from network {} for cloud instance"
                  " {}. {}".format(network, instance, error))

    def get_port(self, instance, network, port):
        """Retrieve specific port by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param network: Network name or ID
        :type netowkr: str
        :param port: Port ID
        :type port: str
        :return: Port information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if network exists and retrieve information
            net_info = self.get_network(ci_info["name"], network)
            if "errors" in net_info:
                return net_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks/{}/"
                    "ports/{}".format(ci_info["name"],
                                      net_info["networkID"],
                                      id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching port with ID {} from network {} for cloud"
                  " instance {}. {}".format(id, network, instance, error))

    def create_network(self, **kwargs):
        """Create network

        :param instance: Instance name or ID
        :type instance: str
        :param type: Type of network
        :type type: str
        :param name: Network name
        :type name: str
        :param cidr: Network in CIDR notation
        :type cidr: str
        :param gateway: Gateway IP address
        :type gateway: str, optional
        :param dns_servers: DNS servers
        :type dns_servers: list, optional
        :param ip_address_ranges: IP address ranges
        :type ip_address_ranges: list, optional
        :return: Network information
        :rtype: dict
        """
        args = ["instance", "type", "name", "cidr"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'type': kwargs.get('type'),
            'name': kwargs.get('name'),
            'cidr': kwargs.get('cidr'),
            'gateway': kwargs.get('gateway'),
            'dns_servers': kwargs.get('dns_servers'),
            'ip_address_ranges': kwargs.get('ip_address_ranges'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                if key == "dns_servers":
                    payload["dnsServers"] = args['dns_servers']
                elif key == "ip_address_ranges":
                    payload["ipAddressRanges"] = args['ip_address_ranges']
                else:
                    payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks".format(
                ci_info["name"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating network for cloud instance {}. {}".format(
                args['instance'], error))

    def create_port(self, **kwargs):
        """Create network

        :param instance: Instance name or ID
        :type instance: str
        :param network: Network name or ID
        :type network: str
        :param description: Description of the port
        :type description: str, optional
        :param ip_address: The requested ip address of this port
        :type ip_address: str, optional
        :return: Port information
        :rtype: dict
        """
        args = ["instance", "network"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'network': kwargs.get('network'),
            'description': kwargs.get('description'),
            'ip_address': kwargs.get('ip_address'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and key != "network" and value is not None:
                if key == "ip_address":
                    payload["ipAddress"] = args['ip_address']
                else:
                    payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if network exists and retrieve information
            net_info = self.get_network(ci_info["name"], args['network'])
            if "errors" in net_info:
                return net_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/networks/{}/ports".format(
                ci_info["name"], net_info["networkID"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating port in network {} for cloud instance {}."
                  " {}".format(args['network'], args['instance'], error))

    def delete_network(self, instance, network):
        """Delete network from cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param network: Network name or ID
        :type network: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if network exists and retrieve information
            net_info = self.get_network(ci_info["name"], network)
            if "errors" in net_info:
                return net_info

            path = ("/pcloud/v1/cloud-instances/{}/networks/{}".format(
                ci_info["name"], net_info["networkID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting network {} from cloud instance {}."
                  " {}".format(network, instance, error))

    def delete_port(self, instance, network, port):
        """Delete port from network

        :param instance: Cloud instance ID
        :type instance: str
        :param network: Network name or ID
        :type network: str
        :param port: Port name or ID
        :type port: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if network exists and retrieve information
            net_info = self.get_network(ci_info["name"], network)
            if "errors" in net_info:
                return net_info

            # Check if port exists and retrieve information
            port_info = self.get_port(ci_info["name"], network)
            if "errors" in net_info:
                return net_info

            path = ("/pcloud/v1/cloud-instances/{}/networks/{}"
                    "/ports/{}".format(ci_info["name"],
                                       net_info["networkID"],
                                       port_info["portID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting port {} from network {} for cloud instance"
                  " {}. {}".format(port, network, instance, error))
