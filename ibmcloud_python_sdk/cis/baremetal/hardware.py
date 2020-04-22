from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import check_args


class Hardware():

    def __init__(self):
        self.client = sl.client()
        self.hw = sl.SoftLayer.HardwareManager(self.client)

    def get_baremetals(self):
        """
        Retrieve baremetal list
        :return: List of baremetal servers
        :rtype: list
        """
        try:
            baremetal = {}
            baremetal["baremetals"] = self.hw.list_hardware()
            return baremetal
        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_baremetal(self, baremetal):
        """
        Retrieve specific baremetal
        :param baremetal: Baremetal name or ID
        :return: Baremetal server information
        :rtype: dict
        """
        by_name = self.get_baremetal_by_name(baremetal)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_baremetal_by_id(baremetal)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_baremetal_by_id(self, id):
        """
        Retrieve specific baremetal by ID
        :param id: baremetal ID
        :return: Baremetal server information
        :rtype: dict
        """
        try:
            return self.hw.get_hardware(id)
        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_baremetal_by_name(self, name):
        """
        Retrieve specific baremetal by name
        :param name: Baremetal name
        :return: Baremetal server information
        :rtype: dict
        """
        try:
            # Retrieve baremetals
            data = self.get_baremetals()

            # Loop over baremetals until filter match
            for baremetal in data["baremetals"]:
                if baremetal["fullyQualifiedDomainName"] == name:
                    # Return data
                    return self.get_baremetal_by_id(baremetal["id"])

            # Return error if no baremetal is found
            return resource_not_found()

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_baremetal_power_state(self, baremetal):
        """
        Retrieve baremetal power state
        :param baremetal: Baremetal name or ID
        :return: Baremetal power state
        :rtype: str
        """
        # Retrieve baremetal info and check is exists
        bm_info = self.get_baremetal(baremetal)
        if "errors" in bm_info:
            return bm_info

        try:
            return self.client.call("Hardware_Server", "getServerPowerState",
                                    id=bm_info["id"])
        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def set_baremetal_power_state(self, **kwargs):
        """
        Set baremetal power state
        :param baremetal: Baremetal name or ID
        :parem power_state: Target power state
        :return: True if the action went well
        :rtype: bool
        """
        args = ["baremetal", "power_state"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'baremetal': kwargs.get('baremetal'),
            'power_state': kwargs.get('power_state'),
        }
        # Retrieve baremetal info and check is exists
        bm_info = self.get_baremetal(args["baremetal"])
        if "errors" in bm_info:
            return bm_info

        switch = {
            "off": "powerOff",
            "on": "powerOn",
            "reboot": "powerCycle",
        }

        if args["power_state"] not in switch:
            return resource_error("state_not_valid",
                                  "available states: {}".format(list(switch)))
        try:
            state = self.client.call("Hardware_Server",
                                     switch.get(args["power_state"]),
                                     id=bm_info["id"])
            if state:
                return {"power_state": args["power_state"]}

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)
