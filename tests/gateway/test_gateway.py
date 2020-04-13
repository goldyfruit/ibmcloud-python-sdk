import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.gateway import Gateway

import tests.common as common
import tests.gateway.custom as custom

class GatewayTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.gateway = Gateway()
        self.fake_gateway = {}
        self.fake_gateway['name'] = 'sdk'
        self.fake_gateway['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_gateway['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_gateway['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_get_call)
    def test_get_gateways(self):
        """Test get_gateways ."""
        response = self.gateway.get_public_gateways()
        self.assertNotEqual(len(response), 0)

#    @patch('ibmcloud_python_sdk.vpc.gateway.Gateway.get_public_gateway_by_name', common.fake_get_call)
#    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_get_call)
#    def test_get_gateway_with_name(self):
#        """Test get_gateway with name as parameter."""
#        response = self.gateway.get_public_gateway(self.fake_gateway['name'])
#        self.assertEqual(response['name'], self.fake_gateway['name'])
#
## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.gateway.gateway.qw', common.fake_get_one)
##    def test_get_gateway_with_id(self):
##        """Test get_gateway with id as parameter."""
##        response = self.gateway.get_gateway(self.fake_gateway['id'])
##        self.assertEqual(response['id'], self.fake_gateway['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_get_one)
#    def test_get_gateway_default_security_group(self):
#        """Test get_gateway_default_security_group."""
#        response = self.gateway.get_gateway_default_security_group(self.fake_gateway['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_gateway['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_get_one)
#    def test_get_gateway_default_network_acl(self):
#        """Test get_gateway_default_network_acl."""
#        response = self.gateway.get_gateway_default_network_acl(self.fake_gateway['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_gateway['default_network_acl'])
#
#    @patch('ibmcloud_python_sdk.vpc.image.Image.get_image', custom.fake_get_image)
    @patch('ibmcloud_python_sdk.vpc.vpc.Vpc.get_vpc', common.fake_get_vpc)
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_create)
    def test_create_gateway_working(self):
        """Test create_gateway should work."""
        response = self.gateway.create_public_gateway(name=self.fake_gateway['name'],

#                resource_group='resource_group',
                vpc='vpc', 
                zone='zone')
        self.assertEqual(response['name'], self.fake_gateway['name'])
 
    @patch('ibmcloud_python_sdk.vpc.vpc.Vpc.get_vpc', common.fake_get_vpc)
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', common.fake_create)
    def test_create_gateway_not_working(self):
        """Test create_gateway should not work."""
        response = self.gateway.create_public_gateway(name=self.fake_gateway['name'],
#                resource_group='resource_group',
                vpc='vpc', 
                zone='zone')
        self.assertNotEqual(response['id'], self.fake_gateway['name'])
       
