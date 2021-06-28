import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args


class ResourceKey():

    def __init__(self):
        self.cfg = params()

    def get_resource_keys(self):
        """Retrieve resource key list

        :return: List of resource keys
        :rtype: list
        """
        try:
            # Connect to api endpoint for resource_keys
            path = "/v2/resource_keys"

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource keys. {}".format(error))
            raise

    def get_resource_key(self, key):
        """Retrieve specific resource key by name or by ID

        :param key: Resource key name or ID
        :type key: str
        :return: Resource key information
        :rtype: dict
        """
        by_name = self.get_resource_key_by_name(key)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_resource_key_by_id(key)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_resource_key_by_id(self, id):
        """Retrieve specific resource key by ID

        :param id: Resource key ID
        :type id: str
        :return: Resource key information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for resource_keys
            path = ("/v2/resource_keys/{}".format(id))

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource key with ID {}. {}".format(
                id, error))
            raise

    def get_resource_key_by_name(self, name):
        """Retrieve specific resource key by name

        :param name: Resource key name
        :type name: str
        :return: Resource key information
        :rtype: dict
        """
        try:
            # Retrieve resource keys
            data = self.get_resource_keys()
            if "errors" in data:
                return data

            # Loop over keys until filter match
            for resource in data['resources']:
                if resource["name"] == name:
                    # Return data
                    return resource

            # Return error if no resource is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching resource key with name {}. {}".format(
                name, error))
            raise

    def create_key(self, **kwargs):
        """Create resource key

        :param name: The new name of the resource group
        :type name: str
        :param source: The short or long ID of resource instance or alias
        :type source: str
        :param parameters: Configuration options represented as key-value
            pairs
        :type parameters: dict optional
        :param role: The role name or it's CRN
        :type: role: str, optional
        """
        args = ["name", "source"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'source': kwargs.get('source'),
            'parameters': kwargs.get('parameters'),
            'role': kwargs.get('role'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                payload[key] = value

        try:
            # Connect to api endpoint for resource_keys
            path = ("/v2/resource_keys")

            # Return data
            return qw("rg", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error create resource key. {}".format(error))
            raise

    def delete_key(self, key):
        """Delete resource key

        :param key: Resource key name or ID
        :type key: str
        :return: Delete status
        :rtype: resource_deleted()
        """
        try:
            # Check if key exists
            key_info = self.get_resource_key(key)
            if "errors" in key_info:
                return key_info

            # Connect to api endpoint resource_keys
            path = ("/v2/resource_keys/{}".format(key_info["id"]))

            data = qw("rg", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting resource key {}. {}".format(key, error))
            raise
