import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.geo import Geo as Region

import tests.common as common


class RegionTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             common.fake_auth)
        self.patcher.start()
        self.region = Region()
        self.fake_region = {}
        self.fake_region['name'] = 'sdk'
        self.fake_region['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_region['default_security_group'] = 'fruit-average-shaping-\
                                                        gone-denture-rumor'
        self.fake_region['default_network_acl'] = 'unpainted-crucial\
                                            -trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.geo.qw', common.fake_get_call)
    def test_get_regions(self):
        """Test get_regions ."""
        response = self.region.get_regions()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.geo.qw', common.fake_get_call)
    def test_get_region_with_name(self):
        """Test get_region with name as parameter."""
        response = self.region.get_region(self.fake_region['name'])
        # print(response)
        self.assertEqual(response['regions'][0]['name'],
                         self.fake_region['name'])

# TODO: to verify
#    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
#    @patch('ibmcloud_python_sdk.region.region.qw', common.fake_get_one)
#    def test_get_region_with_id(self):
#        """Test get_region with id as parameter."""
#        response = self.region.get_region(self.fake_region['id'])
#        self.assertEqual(response['id'], self.fake_region['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.region.qw', common.fake_get_one)
#    def test_get_region_default_security_group(self):
#        """Test get_region_default_security_group."""
#        response = self.region.get_region_default_security_group(
#                   self.fake_region['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'],
#                    self.fake_region['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.region.qw', common.fake_get_one)
#    def test_get_region_default_network_acl(self):
#        """Test get_region_default_network_acl."""
#        response = self.region.get_region_default_network_acl(
#                   self.fake_region['id'])
#        self.assertEqual(response['default_network_acl']['name'],
#                   self.fake_region['default_network_acl'])
#
#    @patch('ibmcloud_python_sdk.vpc.region.qw', common.fake_create)
#    def test_create_region_working(self):
#        """Test create_region should work."""
#        response = self.region.create_region(name=self.fake_region['name'],
#                operating_system='operating_system=',
#                file='file')
#        print(response)
#        self.assertEqual(response['name'], self.fake_region['name'])
#
#    @patch('ibmcloud_python_sdk.vpc.region.qw', common.fake_create)
#    def test_create_region_not_working(self):
#        """Test create_region should not work."""
#        response = self.region.create_region(name=self.fake_region['name'],
#                operating_system='operating_system=',
#                file='file')
#        self.assertNotEqual(response['id'], self.fake_region['name'])
#
