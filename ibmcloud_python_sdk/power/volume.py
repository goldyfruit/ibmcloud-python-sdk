import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import resource_created
from ibmcloud_python_sdk.power import instance
from ibmcloud_python_sdk.power import pvm
from ibmcloud_python_sdk.utils.common import check_args


class Volume():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()
        self.pvm = pvm.Pvm()

    def get_volumes(self, instance):
        """Retrieve volume list from cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: Volume list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/volumes".format(
                ci_info["name"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume list for cloud instance {}."
                  " {}".format(instance, error))

    def get_volume(self, instance, volume):
        """Retrieve specific volume by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param volume: Volume name or ID
        :type volume: str
        :return: Volume information
        :rtype: dict
        """
        by_name = self.get_volume_by_name(instance, volume)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_volume_by_id(instance, volume)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_volume_by_id(self, instance, id):
        """Retrieve specific volume by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param id: Volume ID
        :type id: str
        :return: Volume information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/volumes/{}".format(
                ci_info["name"], id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume with ID {} for cloud instance {}."
                  " {}".format(id, instance, error))

    def get_volume_by_name(self, instance, name):
        """Retrieve specific volume by name

        :param instance: Cloud instance ID
        :type instance: str
        :param name: Volume name
        :type name: str
        :return: Volume information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Retrieve volumes
            data = self.get_volumes(ci_info["name"])
            if "errors" in data:
                return data

            # Loop over volumes until filter match
            for volume in data['volumes']:
                if volume["name"] == name:
                    # Return data
                    return volume

            # Return error if no volume is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching volume with name {} for cloud instance {}."
                  " {}".format(name, instance, error))

    def get_pvm_volumes(self, instance, pvm):
        """Retrieve volumes list for Power Virtual Instance

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :return: PVM volume list
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/volumes".format(ci_info["name"],
                                      pvm_info["pvmInstanceID"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume list for Power Virtual Instance list"
                  " for cloud instance {}. {}".format(instance, error))

    def get_pvm_volume(self, instance, pvm, volume):
        """Retrieve specific volume from Power Virtual Instance by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param volume: Volume name or ID
        :type volume: str
        :return: PVM volume information
        :rtype: dict
        """
        by_name = self.get_pvm_volume_by_name(instance, pvm, volume)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_pvm_volume_by_id(instance, pvm, volume)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_pvm_volume_by_id(self, instance, pvm, id):
        """Retrieve specific volume from Power Virtual Instance by ID
        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param id: Volume ID
        :type id: str
        :return: PVM volume information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(instance, pvm)
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
            print("Error fetching volume with ID {} from Power Virtual"
                  " Instance {} for cloud instance {}. {}".format(
                      id, pvm, instance, error))

    def get_pvm_volume_by_name(self, instance, pvm, name):
        """Retrieve specific volume from Power Virtual Instance by name

        :param instance: Cloud instance ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param name: Volume name
        :type name: str
        :return: PVM volume information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(instance, pvm)
            if "errors" in pvm_info:
                return pvm_info

            # Retrieve volume
            data = self.get_pvm_volumes(ci_info["name"],
                                        pvm_info["pvmInstanceID"])
            if "errors" in data:
                return data

            # Loop over volumes until filter match
            for volume in data['volumes']:
                if volume["name"] == name:
                    # Return data
                    return volume

            # Return error if no volume is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching volume with name {} from Power Virtual"
                  " Instance {} for cloud instance {}. {}".format(
                      name, pvm, instance, error))

    def create_volume(self, **kwargs):
        """Create volume

        :param instance: Cloud instance ID
        :type instance: str
        :param size: Volume size
        :type size: int
        :param name: Volume name
        :type name: str
        :param disk_type: Type of Disk, required if affinity_policy not used
        :type disk_type: str, optional
        :param pool: Volume pool where the volume will be located
        :type pool: str, optional
        :param shareable: Indicates if the volume is shareable between VMs
        :type shareable: str, optional
        :param affinity_policy: Affinity policy for data volume being created;
            requires affinity_volume to be specified
        :type affinity_policy: str, optional
        :param affinity_volume: Volume (ID or Name) to base volume affinity
            policy against; required if affinity_policy provided
        :type affinity_volume: str, optional
        :return: Volume information
        :rtype: dict
        """
        args = ["instance", "size", "name"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'size': kwargs.get('size'),
            'name': kwargs.get('name'),
            'diskType': kwargs.get('disk_type'),
            'volumePool': kwargs.get('pool'),
            'shareable': kwargs.get('shareable'),
            'affinityPolicy': kwargs.get('affinity_policy'),
            'affinityVolume': kwargs.get('affinity_volume'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/volumes".format(
                ci_info["name"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating volume for cloud instance {}. {}".format(
                args['instance'], error))

    def clone_volume(self, **kwargs):
        """Create a clone from a volume

        :param instance: Instance name or ID
        :type instance: str
        :param volumes: List of volumes to be cloned
        :type volumes: list
        :param name: Display name for the new cloned volumes. Cloned Volume
            names will be prefixed with 'clone-'. If multiple volumes cloned
            they will be suffix with a '-' and an incremental number starting
            with 1.
        :type name: str
        :param prefix_name: Prefix to use when naming the new cloned volumes
        :type prefix_name: str, optional
        :return: Volume clone information
        :rtype: dict
        """
        args = ["instance", "volumes", "name"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'volumeIDs': kwargs.get('volumes'),
            'displayName': kwargs.get('name'),
            'namingPrefix': kwargs.get('prefix_name'),
        }

        # Check if cloud instance exists and retrieve information
        ci_info = self.instance.get_instance(args['instance'])
        if "errors" in ci_info:
            return ci_info

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                if key == "volumeIDs":
                    vl = []
                    for volume in args["volumeIDs"]:
                        vol_info = self.get_volume(ci_info["name"], volume)
                        if "errors" in vol_info:
                            return vol_info
                        vl.append(vol_info["volumeID"])
                    payload["volumeIDs"] = vl
                payload[key] = value

        try:
            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/volumes/clone".format(
                ci_info["name"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating clone from volume(s) {} for cloud instance"
                  " {}. {}".format(args["volumeIDs"], args['instance'], error))

    def attach_volume(self, **kwargs):
        """Attach volume to a Power Virtual Instance

        :param instance: Instance name or ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param volume: Volume name or ID
        :type volume: str
        :return: Attachment status
        :rtype: dict
        """
        args = ["instance", "pvm", "volume"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'pvm': kwargs.get('pvm'),
            'volume': kwargs.get('volume'),
        }

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(args['instance'], args['pvm'])
            if "errors" in pvm_info:
                return pvm_info

            # Check if volume exists and retrieve information
            vol_info = self.get_volume(ci_info["name"], args["volume"])
            if "errors" in vol_info:
                return vol_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/volumes/{}".format(ci_info["name"],
                                         pvm_info["pvmInstanceID"],
                                         vol_info["volumeID"]))

            data = qw("power", "POST", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            payload = {"status": "attached"}
            return resource_created(payload)

        except Exception as error:
            print("Error attaching volume {} to Power Virtual Instance {}"
                  " from cloud instance {}. {}".format(
                      args["volume"], args['pvm'], args['instance'], error))

    def detach_volume(self, **kwargs):
        """Detach volume to a Power Virtual Instance

        :param instance: Instance name or ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param volume: Volume name or ID
        :type volume: str
        :return: Dettachement status
        :rtype: dict
        """
        args = ["instance", "pvm", "volume"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'pvm': kwargs.get('pvm'),
            'volume': kwargs.get('volume'),
        }

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(args['instance'], args['pvm'])
            if "errors" in pvm_info:
                return pvm_info

            # Check if volume exists and retrieve information
            vol_info = self.get_volume(ci_info["name"], args["volume"])
            if "errors" in vol_info:
                return vol_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/volumes/{}".format(ci_info["name"],
                                         pvm_info["pvmInstanceID"],
                                         vol_info["volumeID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 202:
                return data["data"]

            # Return status
            payload = {"status": "detached"}
            return resource_deleted(payload)

        except Exception as error:
            print("Error detaching volume {} from Power Virtual Instance {}"
                  " for cloud instance {}. {}".format(
                      args["volume"], args['pvm'], args['instance'], error))

    def boot_volume(self, **kwargs):
        """Set boot volume to a Power Virtual Instance

        :param instance: Instance name or ID
        :type instance: str
        :param pvm: Power Virtual Instance name or ID
        :type pvm: str
        :param volume: Volume name or ID
        :return: Boot status
        :rtype: dict
        """
        args = ["instance", "pvm", "volume"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'pvm': kwargs.get('pvm'),
            'volume': kwargs.get('volume'),
        }

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Check if pvm exists and retrieve information
            pvm_info = self.pvm.get_pvm(args['instance'], args['pvm'])
            if "errors" in pvm_info:
                return pvm_info

            # Check if volume exists and retrieve information
            vol_info = self.get_volume(ci_info["name"], args["volume"])
            if "errors" in vol_info:
                return vol_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/pvm-instances/{}"
                    "/volumes/{}/setboot".format(ci_info["name"],
                                                 pvm_info["pvmInstanceID"],
                                                 vol_info["volumeID"]))

            data = qw("power", "PUT", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            payload = {"status": "booted"}
            return resource_created(payload)

        except Exception as error:
            print("Error setting boot to volume {} from Power Virtual Instance"
                  " {} for cloud instance {}. {}".format(
                      args["volume"], args['pvm'], args['instance'], error))

    def delete_volume(self, instance, volume):
        """Delete volume from cloud instance

        :param instance: Instance name or ID
        :type instance: str
        :param volume: Volume name or ID
        :type volume: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if volume exists and retrieve information
            vol_info = self.get_volume(ci_info["name"], volume)
            if "errors" in vol_info:
                return vol_info

            path = ("/pcloud/v1/cloud-instances/{}/volumes/{}".format(
                ci_info["name"], vol_info["volumeID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting volume {} from cloud instance {}. {}".format(
                volume, instance, error))
