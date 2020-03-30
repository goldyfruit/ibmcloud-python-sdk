import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Key():

    def __init__(self):
        self.cfg = params()

    # Get all keys
    def get_keys(self):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching keys. {error}")
            raise

    # Get specific key by ID or by name
    # This method is generic and should be used as prefered choice
    def get_key(self, key):
        by_name = self.get_key_by_name(key)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_key_by_id(key)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific key by ID
    def get_key_by_id(self, id):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching key with ID {id}. {error}")
            raise

    # Get specific key by name
    def get_key_by_name(self, name):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve keys data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over keys until filter match
            for key in data["keys"]:
                if key["name"] == name:
                    # Return data
                    return key

            # Return error if no key is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching key with name {name}. {error}")
            raise

    # Create key
    def create_key(self, **kwargs):
        # Required parameters
        required_args = set(["public_key"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'public_key': kwargs.get('public_key'),
            'resource_group': kwargs.get('resource_group'),
            'type': kwargs.get('type', 'rsa'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating key. {error}")
            raise

    # Delete key
    # This method is generic and should be used as prefered choice
    def delete_key(self, key):
        by_name = self.delete_key_by_name(key)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.delete_key_by_id(key)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete key by ID
    def delete_key_by_id(self, id):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting key with ID {id}. {error}")
            raise

    # Delete key by name
    def delete_key_by_name(self, name):
        try:
            # Check if key exists
            key = self.get_key_by_name(name)
            if "errors" in key:
                return key

            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                key["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting key with name {name}. {error}")
            raise