import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.vpn import Vpn

import tests.common as common


class VpnTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             common.fake_auth)
        self.patcher.start()
        self.vpn = Vpn()
        self.fake_vpn = {}
        self.fake_vpn['name'] = 'sdk'
        self.fake_vpn['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_vpn['default_security_group'] = "fruit-average-shaping-gone-\
                                                    denture-rumor"
        self.fake_vpn['default_network_acl'] = "unpainted-crucial-trimmer-\
                                                    perennial-zipfile-barcode"

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_get_call)
    def test_get_vpn_gateways(self):
        """Test get_vpns ."""
        response = self.vpn.get_vpn_gateways()
        self.assertNotEqual(len(response), 0)

#    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_get_call)
#    def test_get_vpn_with_name(self):
#        """Test get_vpn with name as parameter."""
#        response = self.vpn.get_vpn(self.fake_vpn['name'])
#        print(response)
#        self.assertEqual(response['name'], self.fake_vpn['name'])
#
# TODO: to verify
#    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
#    @patch('ibmcloud_python_sdk.vpn.vpn.qw', common.fake_get_one)
#    def test_get_vpn_with_id(self):
#        """Test get_vpn with id as parameter."""
#        response = self.vpn.get_vpn(self.fake_vpn['id'])
#        self.assertEqual(response['id'], self.fake_vpn['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_get_one)
#    def test_get_vpn_default_security_group(self):
#        """Test get_vpn_default_security_group."""
#        response = self.vpn.get_\
#                   vpn_default_security_group(self.fake_vpn['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'],
#           self.fake_vpn['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_get_one)
#    def test_get_vpn_default_network_acl(self):
#        """Test get_vpn_default_network_acl."""
#        response = self.vpn.get_vpn_default_network_acl(self.fake_vpn['id'])
#        self.assertEqual(response['default_network_acl']['name'],
#           self.fake_vpn['default_network_acl'])
#
#    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_create)
#    def test_create_vpn_working(self):
#        """Test create_vpn should work."""
#        response = self.vpn.create_vpn(name=self.fake_vpn['name'],
#                operating_system='operating_system=',
#                file='file')
#        print(response)
#        self.assertEqual(response['name'], self.fake_vpn['name'])
#
#    @patch('ibmcloud_python_sdk.vpc.vpn.qw', common.fake_create)
#    def test_create_vpn_not_working(self):
#        """Test create_vpn should not work."""
#        response = self.vpn.create_vpn(name=self.fake_vpn['name'],
#                operating_system='operating_system=',
#                file='file')
#        self.assertNotEqual(response['id'], self.fake_vpn['name'])
