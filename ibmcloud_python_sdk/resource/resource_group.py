import json
import re
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args


class ResourceGroup():

    def __init__(self):
        self.cfg = params()

    def get_resource_groups(self):
        """Retrieve resource group list

        :return: List of resource groups
        :rtype: list
        """
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups"

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource groups. {}".format(error))
            raise

    def get_default_resource_group(self):
        """Retrieve the default resource group

        :return: Default resource group information
        :rtype: dict
        """
        resource_groups = self.get_resource_groups()
        if "errors" in resource_groups:
            return resource_groups

        for resource_group in resource_groups["resources"]:
            if resource_group['default']:
                return resource_group
        # try:
        #     for resource_group in resource_groups:
        #         if resource_group['default']:
        #             return resource_group
        # except Exception as error:
        #     print("Error fetching default resource group. {}".format(error))
        #     raise

    def get_resource_group(self, group):
        """Retrieve specific resource group by name or by ID

        :param group: Resource group name or ID
        :type group: str
        :return: Resource group information
        :rtype: dict
        """
        by_name = self.get_resource_group_by_name(group)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_resource_group_by_id(group)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_resource_group_by_id(self, id):
        """Retrieve specific resource group by ID

        :param id: Resource group ID
        :type id: str
        :return: Resource group information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for resource_groups
            path = ("/v2/resource_groups/{}".format(id))

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource group with ID {}. {}".format(
                id, error))
            raise

    def get_resource_group_by_name(self, name):
        """Retrieve specific resource group by name

        :param name: Resource group name
        :type name: str
        :return: Resource group information
        :rtype: dict
        """
        try:
            # Retrieve resource groups
            data = self.get_resource_groups()
            if "errors" in data:
                return data

            # Loop over resources until filter match
            for resource in data['resources']:
                if resource["name"] == name:
                    # Return data
                    return resource

            # Return error if no resource is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching resource group with name {}. {}".format(
                name, error))
            raise

    def get_resource_groups_by_account(self, id):
        """Retrieve resource group list for a specific account

        :param id: Account ID
        :type id: str
        :return: Resource group information by account
        :rtype: dict
        """
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups?account_id={}".format(id)

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource groups for account {}. {}".format(
                id, error))
            raise

    def get_quota_definitions(self):
        """Retrieve list of all quota definitions

        :return: List of quota definitions
        :rtype: list
        """
        try:
            # Connect to api endpoint for quota_definitions
            path = "/v2/quota_definitions"

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching quota_definitions. {}".format(error))
            raise

    def get_quota_definition(self, quota):
        """Retrieve specific quota definition by name or by ID

        :param quota: Quota definition name or ID
        :type quota: str
        :return: Quota definition
        :rtype: dict
        """
        by_name = self.get_quota_definition_by_name(quota)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                # regex = "Can not find quota definition with id"
                # if re.search(regex, key_name["code"]):
                if key_name["code"] == "not_found":
                    by_id = self.get_quota_definition_by_id(quota)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name



    def get_quota_definition_by_id(self, id):
        """Retrieve specific quota definition by ID

        :param id: Quota definition ID
        :type id: str
        :return: Quota definition
        :rtype: dict
        """
        try:
            # Connect to api endpoint for quota_definitions
            path = ("/v2/quota_definitions/{}".format(id))

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching quota definition with ID {}. {}".format(
                id, error))
            raise

    def get_quota_definition_by_name(self, name):
        """Retrieve specific quota definitnion by name

        :param name: Quota definition name
        :type name: str
        :return: Quota definition
        :rtype: dict
        """
        try:
            # Retrieve quota definitions
            data = self.get_quota_definitions()
            if "errors" in data:
                return data

            # Loop over quota definitions until filter match
            for quota in data['resources']:
                if quota["name"] == name:
                    # Return data
                    return quota

            # Return error if no quota definition is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching quota definition with name {}. {}".format(
                name, error))
            raise

    def create_group(self, **kwargs):
        """Create resource group

        :param name: Name of the resource group
        :type name: str
        :param account_id: The account ID of the resource group
        :type account_id: str
        """
        args = ["name", "account_id"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'account_id': kwargs.get('account_id'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                payload[key] = value

        try:
            # Connect to api endpoint for resource_groups
            path = ("/v2/resource_groups")

            # Return data
            return qw("rg", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error create resource group. {}".format(error))
            raise

    def delete_group(self, group):
        """Delete resource group

        :param group: Resource group name or ID
        :type group:
        :return: Delete status
        :rtype: resource_deleted()
        """
        try:
            # Check if group exists
            group_info = self.get_resource_group(group)
            if "errors" in group_info:
                return group_info

            # Connect to api endpoint resource_groups
            path = ("/v2/resource_groups/{}".format(group_info["id"]))

            data = qw("rg", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting resource group {}. {}".format(group, error))
            raise
