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

    def get_system_roles(self, account):
        """Retrieve system role list per account

        :param account: Account ID
        :type account: str
        :return: List of system roles
        :rtype: list
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v2/roles?account_id={}".format(account))

            # Return data
            return qw("auth", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching system roles for account {}. {}".format(
                account, error))

    def get_system_role(self, account, role):
        """Retrieve specific system role by name or by ID

        :param account: Account ID
        :type account: str
        :param role: Role name or ID
        :type role: str
        :return: System role information
        :rtype: dict
        """
        by_name = self.get_system_role_by_name(account, role)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "role_not_found":
                    by_id = self.get_system_role_by_id(account, role)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_system_role_by_id(self, account, id):
        """Retrieve specific system role by ID

        :param account: Account ID
        :type account: str
        :param id: Role ID
        :type id: str
        :return: System role information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v1/roles/{}?account_id={}".format(id, account))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching system role with ID {}. {}".format(
                id, error))

    def get_system_role_by_name(self, account, name):
        """Retrieve specific system role by name

        :param account: Account ID
        :type account: str
        :param name: Role name
        :type name: str
        :return: System role information
        :rtype: dict
        """
        try:
            # Retrieve roles
            data = self.get_system_roles(account)
            if "errors" in data:
                return data

            # Loop over system roles until filter match
            for role in data['system_roles']:
                if (
                        role.get("display_name") == name
                        or role.get("name", "") == name
                   ):
                    # Return data
                    return role

            # Return error if no system role is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching system role with name {}. {}".format(
                name, error))

    def get_service_roles(self, account, service):
        """Retrieve service role list per account

        :param account: Account ID
        :type account: str
        :param service: Service name
        :type service: str
        :return: List of service roles
        :rtype: list
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v2/roles?account_id={}&format=display"
                    "&service_name={}".format(account, service))

            # Return data
            return qw("auth", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching roles from service {} for account {}."
                  " {}".format(service, account, error))

    def get_service_role(self, account, service, role):
        """Retrieve specific system role by name or by ID

        :param account: Account ID
        :type account: str
        :param service: Service name
        :type service: str
        :param role: Role name or ID
        :type role: str
        :return: Service role information
        :rtype: dict
        """
        by_name = self.get_service_role_by_name(account, service, role)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "role_not_found":
                    by_id = self.get_service_role_by_id(account, service, role)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_service_role_by_id(self, account, service, id):
        """Retrieve specific service role by ID

        :param account: Account ID
        :type account: str
        :param service: Service name
        :type service: str
        :param id: Role ID
        :type id: str
        :return: Service role information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for roles
            path = ("/v2/roles/{}?account_id={}&format=display"
                    "&service_name={}".format(id, account, service))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching role from service {} with ID {}. {}".format(
                service, id, error))

    def get_service_role_by_name(self, account, service, name):
        """Retrieve specific service role by name

        :param account: Account ID
        :type account: str
        :param service: Service name
        :type service: str
        :param name: Role name
        :type name: str
        :return: Service role information
        :rtype: dict
        """
        try:
            # Retrieve service roles
            data = self.get_service_roles(account, service)
            if "errors" in data:
                return data

            # Loop over service roles until filter match
            for role in data['service_roles']:
                if (
                        role.get("display_name") == name
                        or role.get("name", "") == name
                   ):
                    # Return data
                    return role

            # Return error if no service role is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching role from service {} with name {}."
                  " {}".format(service, name, error))

    def create_role(self, **kwargs):
        """Create role

        :param name: The name of the role
        :type name: str
        :param account_id: The account GUID
        :type account_id: str
        :param service_name: The service name
        :type service_name: str
        :param display_name: The display name of the role
        :type display_name: str
        :param actions: The actions of the role
        :type actions: list
        :param description: The description of the role
        :type description: str
        :return: Rolle creation response
        :rtype: dict
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
        :type role: str
        :return: Deletion status
        :rtype: dict
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
