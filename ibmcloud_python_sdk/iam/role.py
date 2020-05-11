import json

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.resource import resource_instance
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted


class Role():

    def __init__(self):
        self.cfg = params()
        self.ri = resource_instance.ResourceInstance()

    def get_roles(self, account):
        """Retrieve role list per account

        :param account: Account ID
        :return List of roles
        :rtype dict
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v2/roles?account_id={}".format(account))

            # Return data
            return qw("auth", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching roles for account {}. {}".format(
                account, error))

    def get_roles_by_service(self, account, service):
        """Retrieve role list per account and per service

        :param account: Account ID
        :param service: Service name
        :return List of roles
        :rtype dict
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v2/roles?account_id={}&format=display"
                    "&service_name={}".format(account, service))

            # Return data
            return qw("auth", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching roles for service {} in account {}."
                  " {}".format(service, account, error))

    def get_role(self, account, role):
        """Retrieve specific role by name or by ID

        :param account: Account ID
        :param role: Role name or ID
        :return Role information
        :rtype dict
        """
        by_name = self.get_role_by_name(account, role)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_role_by_id(account, role)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_role_by_id(self, account, id):
        """Retrieve specific role by ID

        :param account: Account ID
        :param id: Role ID
        :return Role information
        :rtype dict
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v1/roles/{}?account_id={}".format(id, account))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching role with ID {}. {}".format(id, error))
            raise

    def get_role_by_name(self, account, name):
        """Retrieve specific role by name

        :param account: Account ID
        :param name: Role name
        :return Role information
        :rtype dict
        """
        try:
            # Retrieve roles
            data = self.get_roles(account)
            if "errors" in data:
                return data

            # Loop over roles until filter match
            for role in data['system_roles']:
                if role["display_name"] == name:
                    # Return data
                    return role

            # Return error if no role is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching role with name {}. {}".format(name, error))
            raise

    def create_role(self, **kwargs):
        """Create role

        :param name: The name of the role.
        :param account_id: The account GUID.
        :param service_name: The service name.
        :param display_name: The display name of the role.
        :param actions: The actions of the role.
        :param description: The description of the role.
        :return Rolle creation response
        :rtype dict
        """
        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'account_id': kwargs.get('account_id'),
            'service_name': kwargs.get('service_name'),
            'display_name': kwargs.get('display_name'),
            'actions': kwargs.get('actions'),
            'description': kwargs.get('description'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "actions":
                    ac = []
                    for action in args["actions"]:
                        ac.append(action)
                    payload["actions"] = ac
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for roles
            path = "/v2/roles"

            # Return data
            return qw("auth", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating role. {}".format(error))

    def delete_role(self, role):
        """Delete role

        :param role: Role name or ID
        :return Deletion status
        :rtype dict
        """
        # Check if role exists and get information
        role_info = self.get_role(role)
        if "errors" in role_info:
            return role_info

        try:
            # Connect to api endpoint for roles
            path = ("/v1/roles/{}".format(role_info["id"]))

            data = qw("auth", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting polirolecy {}. {}".format(role, error))
