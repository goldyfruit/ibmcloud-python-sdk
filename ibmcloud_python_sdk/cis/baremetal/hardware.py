from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import check_args


class Hardware():

    def __init__(self):
        self.client = sl.client()
        self.hw = sl.SoftLayer.HardwareManager(self.client)

    def get_baremetals(self):
        """Retrieve baremetal list

        :return: List of baremetal servers
        :rtype: dict
        """
        # Display all the fields.
        mask = ""
        try:
            baremetal = {}
            baremetal["baremetals"] = self.hw.list_hardware(mask=mask)

            return baremetal

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_baremetal(self, baremetal):
        """Retrieve specific baremetal

        :param baremetal: Baremetal name or ID
        :type baremetal: str
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
        """Retrieve specific baremetal by ID

        :param id: Baremetal ID
        :type id: str
        :return: Baremetal server information
        :rtype: dict
        """
        try:
            return self.hw.get_hardware(id)

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_baremetal_by_name(self, name):
        """Retrieve specific baremetal by name

        :param name: Baremetal name
        :type name: str
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
        """Retrieve baremetal power state

        :param baremetal: Baremetal name or ID
        :type baremetal: str
        :return: Baremetal power state
        :rtype: dict
        """
        # Retrieve baremetal info and check is exists
        bm_info = self.get_baremetal(baremetal)
        if "errors" in bm_info:
            return bm_info

        try:
            state = self.client.call("Hardware_Server", "getServerPowerState",
                                     id=bm_info["id"])
            return {"power_state": state}

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def set_baremetal_power_state(self, **kwargs):
        """Set baremetal power state

        :param baremetal: Baremetal name or ID
        :type baremetal: str
        :parem power_state: Target power state
        :type power_state: str
        :return: Power state
        :rtype: dict
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

    def reload_os(self, **kwargs):
        """Reload operating system and configuration

        :param baremetal: Baremetal name or ID
        :type baremetal: str
        :param spare_pool: Server will be moved into the spare pool after an
            sperating system reload
        :type spare_pool: str, optional
        :param script: Will be used to download and execute a customer defined
            script on the host at the end of provisioning
        :type script: str, optional
        :param retention: Primary drive will be converted to a portable
            storage volume during an operating system reload
        :type retention: str
        :param erase_drives: All data will be erased from drives during an
            sperating system reload
        :type erase_drives: bool, optional
        :param hard_drives: The hard drive partitions that a server can be
            partitioned with
        :param image_template_id: An image template ID that will be deployed
            to the host. If provided no item prices are required
        :type image_template_id: str, optional
        :param item_prices: Item prices that the server can be configured with
        :type item_prices: list, optional
        :param enable_lvm: The provision should use LVM for all logical drives
        :type enable_lvm: bool, optional
        :param reset_ipmi_password: The remote management cards password will
            be reset
        :type reset_ipmi_password: bool, optional
        :param ssh_keys: SSH keys to add to the server for authentication.
            SSH Keys will not be added to servers with Microsoft Windows
        :type ssh_keys: list, optional
        :param upgrade_bios: BIOS will be updated when installing the
            operating system.
        :type upgrade_bios: bool, optional
        :param upgrade_firmware: Firmware on all hard drives will be updated
            when installing the operating system
        :type upgrade_firmware: bool, optional
        :return: Reload status
        :rtype: dict
        """
        args = ["baremetal"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'baremetal': kwargs.get('baremetal'),
            'spare_pool': kwargs.get('spare_pool'),
            'script': kwargs.get('provision_script_uri'),
            'retention': kwargs.get('drive_retention'),
            'erase_drives': kwargs.get('erase_drives'),
            'hard_drives': kwargs.get('hard_drives'),
            'image_template_id': kwargs.get('image_template_id'),
            'item_prices': kwargs.get('item_prices'),
            'enable_lvm': kwargs.get('enable_lvm'),
            'reset_ipmi_password': kwargs.get('reset_ipmi_password'),
            'ssh_keys': kwargs.get('ssh_keys'),
            'upgrade_bios': kwargs.get('upgrade_bios'),
            'upgrade_firmware': kwargs.get('upgrade_firmware'),
        }

        # Retrieve baremetal info and check is exists
        bm_info = self.get_baremetal(args['baremetal'])
        if "errors" in bm_info:
            return bm_info

        config = {}
        for key, value in args.items():
            if key != "baremetal" and value is not None:
                if key == "spare_pool":
                    config["addToSparePoolAfterOsReload"] = 1
                elif key == "script":
                    config["customProvisionScriptUri"] = args['script']
                elif key == "retention":
                    config["driveRetentionFlag"] = 1
                elif key == "erase_drives":
                    config["eraseHardDrives"] = 1
                elif key == "hard_drives":
                    config["hardDrives"] = args['hard_drives']
                elif key == "image_template_id":
                    config["imageTemplateId"] = args['image_template_id']
                elif key == "item_prices":
                    ip = []
                    for item in args["item_prices"]:
                        tmp_i = {}
                        tmp_i["id"] = item
                        ip.append(tmp_i)
                    config["itemPrices"] = ip
                elif key == "enable_lvm":
                    config["lvmFlag"] = 1
                elif key == "reset_ipmi_password":
                    config["resetIpmiPassword"] = 1
                elif key == "ssh_keys":
                    kp = []
                    for key_pair in args["ssh_keys"]:
                        kp.append(key_pair)
                    config["sshKeyIds"] = kp
                elif key == "upgrade_bios":
                    config["upgradeBios"] = 1
                elif key == "upgrade_firmware":
                    config["upgradeHardDriveFirmware"] = 1

        try:
            state = self.client['Hardware_Server'].reloadOperatingSystem(
                        'FORCE', config, id=bm_info["id"])

            if state:
                return {"reload_os_status": "requested"}

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)
