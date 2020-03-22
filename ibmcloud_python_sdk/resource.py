import http.client
import json
from . import config as ic


class Resource():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn_rg = self.cfg.conn_rg

    # Get all resource groups
    def get_resource_groups(self):
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups"
            self.conn_rg.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn_rg.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching resource groups. {error}")
            raise

    # Get resource groups by account
    def get_resource_groups_by_account(self, id):
        try:
            # Connect to api endpoint for resource_groups
            path = f"/v2/resource_groups?account_id={id}"
            self.conn_rg.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn_rg.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching resource groups for account {id}. {error}")
            raise
