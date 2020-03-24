

class Geo():

    def __init__(self):
        self.cfg = ic_con.Config()
        self.common = ic_com.Common()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers

    # Get all regions
    def get_regions(self):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions?version={}&generation={}").format(
                self.ver, self.gen)

            # Return response data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)

        except Exception as error:
            print(f"Error fetching regions. {error}")
            raise

    # Get specific region by name
    def get_region(self, name):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}?version={}&generation={}").format(
                name, self.ver, self.gen)

            # Return response data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)

        except Exception as error:
            print(f"Error fetching region with name {name}. {error}")
            raise

    # Get all zones from a region
    def get_region_zones(self, region):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones?version={}&generation={}").format(
                region, self.ver, self.gen)

            # Return response data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)

        except Exception as error:
            print(f"Error fetching zones for region {region}. {error}")
            raise

    # Get specific zone from a region
    def get_region_zone(self, region, zone):
        try:
            # Connect to api endpoint for regions
            path = ("/v1/regions/{}/zones/{}?version={}&generation={}").format(
                region, zone, self.ver, self.gen)

            # Return response data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)

        except Exception as error:
            print(f"Error fetching zone {zone} for region {region}. {error}")
            raise
