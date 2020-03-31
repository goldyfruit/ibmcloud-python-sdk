import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.resource import Resource

from .. import common as common

class ResourceTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.resource = Resource()
        self.fake_resource = {}
        self.fake_resource['name'] = 'sdk'
        self.fake_resource['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_resource['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_resource['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_get_call)
    def test_get_resources(self):
        """Test get_resources ."""
        response = self.resource.get_resource_groups()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_get_call)
    def test_get_resource_with_name(self):
        """Test get_resource with name as parameter."""
        response = self.resource.get_resource_groups_by_account(self.fake_resource['name'])
        print(response)
        self.assertEqual(response['resource_groups'][0]['name'], self.fake_resource['name'])

## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.resource.resource.qw', common.fake_get_one)
##    def test_get_resource_with_id(self):
##        """Test get_resource with id as parameter."""
##        response = self.resource.get_resource(self.fake_resource['id'])
##        self.assertEqual(response['id'], self.fake_resource['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_get_one)
#    def test_get_resource_default_security_group(self):
#        """Test get_resource_default_security_group."""
#        response = self.resource.get_resource_default_security_group(self.fake_resource['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_resource['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_get_one)
#    def test_get_resource_default_network_acl(self):
#        """Test get_resource_default_network_acl."""
#        response = self.resource.get_resource_default_network_acl(self.fake_resource['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_resource['default_network_acl'])
#
#    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_create)
#    def test_create_resource_working(self):
#        """Test create_resource should work."""
#        response = self.resource.create_resource(name=self.fake_resource['name'], 
#                operating_system='operating_system=', 
#                file='file')
#        print(response)
#        self.assertEqual(response['name'], self.fake_resource['name'])
# 
#    @patch('ibmcloud_python_sdk.vpc.resource.qw', common.fake_create)
#    def test_create_resource_not_working(self):
#        """Test create_resource should not work."""
#        response = self.resource.create_resource(name=self.fake_resource['name'],
#                operating_system='operating_system=', 
#                file='file')
#        self.assertNotEqual(response['id'], self.fake_resource['name'])
#      
