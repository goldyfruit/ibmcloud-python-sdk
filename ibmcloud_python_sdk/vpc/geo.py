from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Geo():

    def __init__(self):
        self.cfg = params()

    def get_regions(self):
        """Retrieve region list.

        :raise: Exception if unable to fetch regions
        :return: List of regions
        :rtype: dict
        """
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching regions. {}".format(error))
            raise

    def get_region(self, region):
        """Retrieve specific region

        :param region: Region name
        :raise: Exception if unable to fetch region
        :return: Region information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}?version={}&generation={}".format(
                region, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching region {}. {}".format(region, error))
            raise

    def get_region_zones(self, region):
        """Retrieve zone list for a specific region

        :param region: Region name
        """
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones?version={}&generation={}".format(
                region, self.cfg["version"], self.cfg["generation"]))
            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching zones for region {}. {}".format(
                region, error))
            raise

    # Get specific zone from a region
    def get_region_zone(self, region, zone):
        """Retrieve specific zone for a specific region

        :param region: Region name
        :param zone: Zone name
        """
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones/{}?version={}&generation={}".format(
                region, zone, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching zone {} for region {}. {}".format(
                zone, region, error))
            raise
