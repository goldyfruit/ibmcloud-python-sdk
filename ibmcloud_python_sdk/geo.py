import json
from . import config as ic


class Geo():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn = self.cfg.conn

    # Get all regions
    def get_regions(self):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching regions. {error}")
            raise

    # Get specific region by name
    def get_region(self, name):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}?version={}&generation={}").format(
                name, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching region with name {name}. {error}")
            raise

    # Get all zones from a region
    def get_region_zones(self, region):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones?version={}&generation={}").format(
                region, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching zones for region {region}. {error}")
            raise

    # Get specific zone from a region
    def get_region_zone(self, region, zone):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones/{}?version={}&generation={}").format(
                region, zone, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching zone {zone} for region {region}. {error}")
            raise
