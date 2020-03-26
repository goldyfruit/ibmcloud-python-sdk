from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Geo():

    def __init__(self):
        self.cfg = params()

    # Get all regions
    def get_regions(self):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching regions. {error}")
            raise

    # Get specific region by name
    def get_region(self, name):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}?version={}&generation={}").format(
                name, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching region with name {name}. {error}")
            raise

    # Get all zones from a region
    def get_region_zones(self, region):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones?version={}&generation={}").format(
                region, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching zones for region {region}. {error}")
            raise

    # Get specific zone from a region
    def get_region_zone(self, region, zone):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones/{}?version={}&generation={}").format(
                region, zone, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching zone {zone} for region {region}. {error}")
            raise
