import http.client
import json
from . import config as ic

from . import config as ic_con
from . import common as ic_com


class Resource():

    def __init__(self):
        self.cfg = ic_con.Config()
        self.common = ic_com.Common()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers

    # Get all resource groups
    def get_resource_groups(self):
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups"

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching resource groups. {error}")
            raise

    # Get resource groups by account
    def get_resource_groups_by_account(self, id):
        try:
            # Connect to api endpoint for resource_groups
            path = f"/v2/resource_groups?account_id={id}"

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching resource groups for account {id}. {error}")
            raise
