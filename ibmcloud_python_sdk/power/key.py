import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args


class Key():

    def __init__(self):
        self.cfg = params()

    def get_keys(self, tenant):
        """Retrieve keys for a specific tenant

        :param tenant: Tenant ID (Account ID)
        :type tenant: str
        :return: List of keys
        :rtype: list
        """
        try:
            # Connect to api endpoint for sshkeys
            path = ("/pcloud/v1/tenants/{}/sshkeys".format(tenant))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching keys for tenant {}. {}".format(
                tenant, error))

    def get_key(self, tenant, key):
        """Retrieve specific key for a specific tenant

        :param tenant: Tenant ID (Account ID)
        :type tenant: str
        :param key: Key name
        :type key: str
        :return: Key information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for sshkeys
            path = ("/pcloud/v1/tenants/{}/sshkeys/{}".format(tenant, key))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching key {} for tenant {}. {}".format(
                key, tenant, error))

    def create_key(self, **kwargs):
        """Create key

        :param tenant: Tenant ID (Account ID)
        :type tenant: str
        :param name: User defined name for the SSH key
        :type name: str
        :param public_key: A unique public SSH key to import
        :type public_key: str
        :return: Key information
        :rtype: dict
        """
        args = ["tenant", "name", "public_key"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'tenant': kwargs.get('tenant'),
            'name': kwargs.get('name'),
            'public_key': kwargs.get('public_key'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "tenant" and value is not None:
                if key == "public_key":
                    payload["sshKey"] = args['public_key']
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for sshkeys
            path = ("/pcloud/v1/tenants/{}/sshkeys".format(args['tenant']))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating key. {}".format(error))

    def delete_key(self, tenant, key):
        """Delete key

        :param tenant: Tenant ID (Account ID)
        :type tenant: str
        :param key: Key name
        :type key: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            # Check if key exists
            key_info = self.get_key(tenant, key)
            if "errors" in key_info:
                return key_info

            # Connect to api endpoint for sshkeys
            path = ("/pcloud/v1/tenants/{}/sshkeys/{}".format(
                tenant, key_info["name"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting key {}. {}".format(key, error))
