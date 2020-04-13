import http.client
import json
from . import config as ic

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found


class Resource():

    def __init__(self):
        self.cfg = params()

    def get_resource_groups(self):
        """
        Retrieve resource group list
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
        """
        Retrieve the default resource group
        """
        resource_groups = self.get_resource_groups()["resources"]
        try:
            for resource_group in resource_groups:
                if resource_group['default'] == True:
                    return resource_group
        except Exception as error:
            print("Error fetching default resource group. {}".format(error))
            raise

    def get_resource_group(self, group):
        """
        Retrieve specific resource group by name or by ID
        :param group: Resource group name or ID
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
        """
        Retrieve specific resource group by ID
        :param id: Resource group ID
        """
        try:
            # Connect to api endpoint for resource_groups
            path = ("/v2/resource_groups/{}").format(id)

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource group with ID {}. {}").format(
                id, error)
            raise

    def get_resource_group_by_name(self, name):
        """
        Retrieve specific resource group by name
        :param name: Resource group name
        """
        try:
            # Connect to api endpoint for resource_groups
            path = ("/v2/resource_groups")

            # Retrieve resources data
            data = qw("rg", "GET", path, headers())["data"]

            # Loop over resources until filter match
            for resource in data['resources']:
                if resource["name"] == name:
                    # Return data
                    return resource

            # Return error if no resource is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching resource group with name {}. {}").format(
                name, error)
            raise

    # Get resource groups by account
    def get_resource_groups_by_account(self, id):
        """
        Retrieve resource group list for a specific account
        :param id: Account ID
        """
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups?account_id={}".format(id)

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource groups for account {}. {}").format(
                id, error)
            raise
