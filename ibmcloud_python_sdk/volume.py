import json
from . import config as ic_con
from . import common as ic_com


class Volume():

    def __init__(self):
        self.cfg = ic_con.Config()
        self.common = ic_com.Common()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers

    # Get all volume profiles
    def get_volume_profiles(self):
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles?version={}&generation={}").format(
                self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching volume profiles. {error}")
            raise

    # Get specific volume profile
    def get_volume_profile(self, name):
        try:
            # Connect to api endpoint for volume
            path = ("/v1/volume/profiles/{}?version={}"
                    "&generation={}").format(name, self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching volume profile with name {name}. {error}")
            raise

    # Get all volumes
    def get_volumes(self):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes?version={}&generation={}").format(
                self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching volumes. {error}")
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
                id, self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching volume with ID {id}. {error}")
            raise

    # Get specific volume by name
    def get_volume_by_name(self, name):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/?version={}&generation={}").format(
                self.ver, self.gen)

            # Retrieve volumes data
            data = self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

            # Loop over volumes until filter match
            for volume in data["volumes"]:
                if volume['name'] == name:
                    # Return response data
                    return volume

            # Return error if no volume is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching volume with name {name}. {error}")
            raise

    # Create volume
    def create_volume(self, **kwargs):
        # Required parameters
        required_args = set(["profile", "zone", "capacity"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
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
                self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "POST", path, self.headers,
                json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating volume. {error}")
            raise

    # Delete volume
    # This method is generic and should be used as prefered choice
    def delete_volume(self, volume):
        by_name = self.delete_volume_ip_by_name(volume)
        if "errors" in by_name:
            for key_volume in by_name["errors"]:
                if key_volume["code"] == "not_found":
                    by_id = self.delete_volume_ip_by_id(volume)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete volume by ID
    def delete_volume_ip_by_id(self, id):
        try:
            # Connect to api endpoint for volumes
            path = ("/v1/volumes/{}?version={}&generation={}").format(
                id, self.ver, self.gen)

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting volume with ID {id}. {error}")
            raise

    # Delete volume by name
    def delete_volume_ip_by_name(self, name):
        try:
            # Check if volume exists
            volume = self.get_volume_by_name(name)
            if "errors" in volume:
                return volume

            # Connect to api endpoint for volumes
            path = ("/v1/volumes/{}?version={}&generation={}").format(
                volume["id"], self.ver, self.gen)

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting volume with name {name}. {error}")
            raise
