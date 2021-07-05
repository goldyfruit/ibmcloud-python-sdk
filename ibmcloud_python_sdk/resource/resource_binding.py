import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args


class ResourceBinding():

    def __init__(self):
        self.cfg = params()

    def get_resource_bindings(self):
        """Retrieve resource binding list

        :return: List of resource bindings
        :rtype: list
        """
        try:
            # Connect to api endpoint for resource_bindings
            path = "/v2/resource_bindings"

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource bindings. {}".format(error))
            raise

    def get_resource_binding(self, binding):
        """Retrieve specific resource binding by name or by ID

        :param binding: Resource binding name or ID
        :type binding: str
        :return: Resource binding information
        :rtype: dict
        """
        by_name = self.get_resource_binding_by_name(binding)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_resource_binding_by_id(binding)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_resource_binding_by_id(self, id):
        """Retrieve specific resource binding by ID

        :param id: Resource binding ID
        :type id: str
        :return: Resource binding information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for resource_bindings
            path = ("/v2/resource_bindings/{}".format(id))

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource binding with ID {}. {}".format(
                id, error))
            raise

    def get_resource_binding_by_name(self, name):
        """Retrieve specific resource binding by name

        :param name: Resource binding name
        :type name: str
        :return: Resource binding information
        :rtype: dict
        """
        try:
            # Retrieve resource bindings
            data = self.get_resource_bindings()
            if "errors" in data:
                return data

            # Loop over bindings until filter match
            for resource in data['resources']:
                if resource["name"] == name:
                    # Return data
                    return resource

            # Return error if no resource is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching resource binding with name {}. {}".format(
                name, error))
            raise

    def create_binding(self, **kwargs):
        """Create resource binding

        :param name: The new name of the resource group
        :type name: str
        :param target: The CRN of application to bind to in a specific
            environment
        :type target: str
        :param source: The short or long ID of resource instance or alias
        :type source: str
        :param parameters: Configuration options represented as key-value
            pairs
        :type parameters: dict, optional
        :param role: The role name or it's CRN
        :type role: str, optional
        """
        args = ["name", "target", "source"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'target': kwargs.get('target'),
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
            # Connect to api endpoint for resource_bindings
            path = ("/v2/resource_bindings")

            # Return data
            return qw("rg", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error create resource binding. {}".format(error))
            raise

    def delete_binding(self, binding):
        """Delete resource binding

        :param binding: Resource binding name or ID
        :type binding: str
        :return: Delete status
        :rtype: resource_deleted()
        """
        try:
            # Check if binding exists
            binding_info = self.get_resource_binding(binding)
            if "errors" in binding_info:
                return binding_info

            # Connect to api endpoint resource_bindings
            path = ("/v2/resource_bindings/{}".format(binding_info["id"]))

            data = qw("rg", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting resource binding {}. {}".format(
                binding, error))
            raise
