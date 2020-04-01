import http.client
import json
from . import config as ic

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


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
            print(f"Error fetching resource groups. {error}")
            raise

    # Get resource groups by account
    def get_resource_groups_by_account(self, id):
        """
        Retrieve resource group list for a specific account
        :param id: Account ID
        """
        try:
            # Connect to api endpoint for resource_groups
            path = f"/v2/resource_groups?account_id={id}"

            # Return data
            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching resource groups for account {id}. {error}")
            raise
