import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Dns():

    def __init__(self):
        self.cfg = params()

    def get_dns_instances(self):
        """
        Retrieve all dns instances
        """
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances")

            # Return data
            return qw("rg", "GET", path, headers())
        except Exception as error:
            print("Error fetching resource instances. {}").format(error)
            raise

    def get_zones(self):
        """
        Retrieve all zones
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("")

            # Return data
            return qw("dns", "GET", path, headers())
        except Exception as error:
            print("Error fetching dns zones. {}").format(error)
            raise

    def test(self):
        print(self.cfg)
