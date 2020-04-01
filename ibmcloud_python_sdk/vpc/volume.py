import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args


class Volume():

    def __init__(self):
        self.cfg = params()

    # Get all volume profiles
    def get_volume_profiles(self):
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume profiles. {}").format(error)
            raise

    # Get specific volume profile
    def get_volume_profile(self, name):
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles/{}?version={}"
                    "&generation={}").format(name, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume profile {}. {}").format(profile,
                                                                 error)
            raise

    # Get all volumes
    def get_volumes(self):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volumes. {}").format(error)
            raise

    # Get specific volume by ID or by name
    # This method is generic and should be used as prefered choice
    def get_volume(self, volume):
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

    # Get specific volume by ID
    def get_volume_by_id(self, id):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume with ID {}. {}").format(id, error)
            raise

    # Get specific volume by name
    def get_volume_by_name(self, name):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve volumes data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over volumes until filter match
            for volume in data["volumes"]:
                if volume["name"] == name:
                    # Return response data
                    return volume

            # Return error if no volume is found
            return resource_not_found

        except Exception as error:
            print("Error fetching volume with name {}. {}").format(name,
                                                                   error)
            raise

    # Create volume
    def create_volume(self, **kwargs):
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
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "profile":
                payload["profile"] = {"name": args["profile"]}
            elif key == "zone":
                payload["zone"] = {"name": args["zone"]}
            else:
                payload[key] = value

        print(payload)
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
            return resource_deleted

        except Exception as error:
            print("Error deleting volume {}. {}").format(volume, error)
            raise
