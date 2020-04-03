import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk import resource_group


class Volume():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.Resource()

    def get_volume_profiles(self):
        """
        Retrieve volume profile list
        """
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume profiles. {}").format(error)
            raise

    def get_volume_profile(self, profile):
        """
        Retrieve specific volume profile
        :param profile: Volume profile name
        """
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles/{}?version={}"
                    "&generation={}").format(profile, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume profile {}. {}").format(profile,
                                                                 error)
            raise

    def get_volumes(self):
        """
        Retrieve volume list
        :param profile: Volume profile name
        """
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volumes. {}").format(error)
            raise

    def get_volume(self, volume):
        """
        Retrieve specific volume by name or by ID
        :param volume: Volume name or ID
        """
        by_name = self.get_volume_by_name(volume)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_volume_by_id(volume)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_volume_by_id(self, id):
        """
        Retrieve specific volume by ID
        :param id: Volume ID
        """
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume with ID {}. {}").format(id, error)
            raise

    def get_volume_by_name(self, name):
        """
        Retrieve specific volume by name
        :param name: Volume name
        """
        try:
            # Retrieve volumes
            data = self.get_volumes()
            if "errors" in data:
                return data

            # Loop over volumes until filter match
            for volume in data["volumes"]:
                if volume["name"] == name:
                    # Return response data
                    return volume

            # Return error if no volume is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching volume with name {}. {}").format(name,
                                                                   error)
            raise

    def create_volume(self, **kwargs):
        """
        Create block volume
        :param name: Optional. The unique user-defined name for this volume.

        :param resource_group: Optional. The resource group to use.

        :param zone: The location of the volume.

        :param iops: Optional. The bandwidth for the volume.

        :param profile: The profile to use for this volume.

        :param capacity: The capacity of the volume in gigabytes.
        """
        args = ["profile", "zone", "capacity"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'zone': kwargs.get('zone'),
            'iops': kwargs.get('iops'),
            'resource_group': kwargs.get('resource_group'),
            'profile': kwargs.get('profile'),
            'capacity': kwargs.get('capacity'),
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
                elif key == "profile":
                    payload["profile"] = {"name": args["profile"]}
                elif key == "zone":
                    payload["zone"] = {"name": args["zone"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating volume. {}").format(error)
            raise

    def delete_volume(self, volume):
        """
        Delete volume
        :param volume: Volume name or ID
        """
        # Check if volume exists and get information
        volume_info = self.get_volume(volume)
        if "errors" in volume_info:
            return volume_info

        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/{}?version={}&generation={}").format(
                volume_info["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting volume {}. {}").format(volume, error)
            raise
