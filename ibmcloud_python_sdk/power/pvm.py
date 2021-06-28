import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.power import instance
from ibmcloud_python_sdk.utils.common import check_args


class Pvm():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_pvms(self, instance):
        """Retrieve Power Virtual Instance list for specific cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: PVM list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances".format(
                ci_info["name"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching Power Virtual Instance list for cloud"
                  " instance {}. {}".format(instance, error))

    def get_pvm(self, instance, pvm):
        """Retrieve specific Power Virtual Instance by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :return: PVM information
        :rtype: dict
        """
        by_name = self.get_pvm_by_name(instance, pvm)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_pvm_by_id(instance, pvm)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_pvm_by_id(self, instance, id):
        """Retrieve specific Power Virtual Instance by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param id: Power Virtual Instance ID
        :type id: str
        :return: PVM information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}".format(
                ci_info["name"], id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching Power Virtual Instance with ID {} for cloud"
                  " instance {}. {}".format(id, instance, error))

    def get_pvm_by_name(self, instance, name):
        """Retrieve specific Power Virtual Instance by name

        :param instance: Cloud instance ID
        :type instance: str
        :param name: Power Virtual Instance name
        :type name: str
        :return: PVM information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Retrieve pvms
            data = self.get_pvms(ci_info["name"])
            if "errors" in data:
                return data

            # Loop over pvms until filter match
            for pvm in data['pvmInstances']:
                if pvm["serverName"] == name:
                    # Return data
                    return pvm

            # Return error if no pvm is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching Power Virtual Instance with name {} for"
                  " cloud instance {}. {}".format(name, instance, error))

    def get_pvm_networks(self, instance, pvm):
        """Retrieve networks list for Power Virtual Instance

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :return: PVM network list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/networks".format(ci_info["name"],
                                       pvm_info["pvmInstanceID"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network list for Power Virtual Instance list"
                  " for cloud instance {}. {}".format(instance, error))

    def get_pvm_network(self, instance, pvm, network):
        """Retrieve specific network from Power Virtual Instance by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param network: Network name or ID
        :type network: str
        :return: PVM network information
        :rtype: dict
        """
        by_name = self.get_pvm_network_by_name(instance, pvm, network)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_pvm_network_by_id(instance, pvm, network)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_pvm_network_by_id(self, instance, pvm, id):
        """Retrieve specific network from Power Virtual Instance by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param id: Network ID
        :type id: str
        :return: PVM network information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/networks/{}".format(ci_info["name"],
                                          pvm_info["pvmInstanceID"],
                                          id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network with ID {} from Power Virtual"
                  " Instance {} for cloud instance {}. {}".format(
                      id, pvm, instance, error))

    def get_pvm_network_by_name(self, instance, pvm, name):
        """Retrieve specific Power Virtual Instance by name

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param name: Network name
        :type name: str
        :return: PVM network information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Retrieve networks
            data = self.get_pvm_networks(ci_info["name"],
                                         pvm_info["pvmInstanceID"])
            if "errors" in data:
                return data

            # Loop over network until filter match
            for network in data['networks']:
                if network["networkName"] == name:
                    # Return data
                    return network

            # Return error if no network is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching network with name {} from Power Virtual"
                  " Instance {} for cloud instance {}. {}".format(
                      name, pvm, instance, error))

    def perform_action(self, **kwargs):
        """Perform an action on Power Virtual Machine

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param action: Name of the action to take
        :type action: str
        :return: Action information
        :rtype: dict
        """
        args = ["instance", "pvm", "action"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'pvm': kwargs.get('pvm'),
            'action': kwargs.get('action'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and key != "pvm" and value is not None:
                payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(ci_info["name"], args['pvm'])
            if "errors" in pvm_info:
                return pvm_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/action".format(ci_info["name"],
                                     pvm_info["pvmInstanceID"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error performing action {} on Power Virtual Machine {} for"
                  " cloud instance {}. {}".format(args['action'],
                                                  args['network'],
                                                  args['instance'], error))

    def delete_pvm(self, instance, pvm):
        """Delete Power Virtual Instance

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}".format(
                ci_info["name"], pvm_info["pvmInstanceID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting Power Virtual Instance {} from cloud"
                  " instance {}. {}".format(pvm, instance, error))

    def delete_pvm_network(self, instance, pvm, network):
        """Delete Power Virtual Instance network

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param network: Network name or ID
        :type network: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            net_info = self.get_pvm_network(ci_info["name"],
                                            pvm_info["pvmInstanceID"],
                                            network)
            if "errors" in net_info:
                return net_info

            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/networks/{}".format(ci_info["name"],
                                          pvm_info["pvmInstanceID"],
                                          net_info["networkID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting network {} from Power Virtual Instance {}"
                  " for cloud instance {}. {}".format(
                      network, pvm, instance, error))
