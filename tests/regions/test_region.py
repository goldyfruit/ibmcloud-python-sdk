import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.geo import Geo as Region

from tests.Region import Region as region
from tests.Zone import Zone as zone
from tests.Common import Common as Common

class RegionTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             region.authentication)
        self.patcher.start()
        self.region = Region()

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.geo.qw', region.qw)
    def test_get_regions(self):
        """Test get_regions."""
        response = self.region.get_regions()
        self.assertNotEqual(len(response["regions"]), 0)

    @patch('ibmcloud_python_sdk.vpc.geo.qw', region.return_exception)
    def test_get_regions_error_by_exception(self):
        """Test get_regions (error by exception)."""
        with self.assertRaises(Exception):
            response = self.region.get_regions()

    @patch('ibmcloud_python_sdk.vpc.geo.qw', region.qw)
    def test_get_region(self):
        """Test get_region with name as parameter."""
        response = self.region.get_region(region.name)
        self.assertNotEqual(len(response["name"]), region.name)

    @patch('ibmcloud_python_sdk.vpc.geo.qw', region.return_exception)
    def test_get_region_error_by_exception(self):
        """Test get_region with name as parameter (return exception)."""
        with self.assertRaises(Exception):
            response = self.region.get_region(region.name)

    @patch('ibmcloud_python_sdk.vpc.geo.qw', zone.qw)
    def test_get_region_zones(self):
        """Test get_region_zones."""
        response = self.region.get_region_zones('us-south')
        self.assertNotEqual(response['zones'], "")

    @patch('ibmcloud_python_sdk.vpc.geo.qw', zone.return_exception)
    def test_get_region_zones_error_by_exception(self):
        """Test get_region_zones (error by exception)."""
        with self.assertRaises(Exception):
            response = self.region.get_region_zones('us-south')

    @patch('ibmcloud_python_sdk.vpc.geo.qw', zone.qw)
    def test_get_region_zone(self):
        """Test get_region_zone."""
        response = self.region.get_region_zone('us-south', zone.name)
        print(response)
        self.assertEqual(response['name'], zone.name)

    @patch('ibmcloud_python_sdk.vpc.geo.qw', zone.return_exception)
    def test_get_region_zone_error_by_exception(self):
        """Test get_region_zone (error by exception)."""
        with self.assertRaises(Exception):
            response = self.region.get_region_zones('us-south', 'random_zone')