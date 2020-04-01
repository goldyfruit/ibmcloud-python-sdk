import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.floating_ip import Fip as FloatingIP

import tests.common as common

class FloatingIPTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.floating_ip = FloatingIP()
        self.fake_floating_ip = {}
        self.fake_floating_ip['name'] = 'sdk'
        self.fake_floating_ip['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_floating_ip['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_floating_ip['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_get_call)
    def test_get_floating_ips(self):
        """Test get_floating_ips ."""
        response = self.floating_ip.get_floating_ips()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_get_call)
    def test_get_floating_ip_with_name(self):
        """Test get_floating_ip with name as parameter."""
        response = self.floating_ip.get_floating_ip(self.fake_floating_ip['name'])
        self.assertEqual(response['name'], self.fake_floating_ip['name'])

## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.foating_ip.floating_ip.qw', common.fake_get_one)
##    def test_get_floating_ip_with_id(self):
##        """Test get_floating_ip with id as parameter."""
##        response = self.floating_ip.get_floating_ip(self.fake_floating_ip['id'])
##        self.assertEqual(response['id'], self.fake_floating_ip['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_get_one)
#    def test_get_floating_ip_default_security_group(self):
#        """Test get_floating_ip_default_security_group."""
#        response = self.floating_ip.get_floating_ip_default_security_group(self.fake_floating_ip['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_floating_ip['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_get_one)
#    def test_get_floating_ip_default_network_acl(self):
#        """Test get_floating_ip_default_network_acl."""
#        response = self.floating_ip.get_floating_ip_default_network_acl(self.fake_floating_ip['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_floating_ip['default_network_acl'])
#
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_create)
    def test_reserve_floating_ip_working(self):
        """Test reserve_floating_ip should work."""
        response = self.floating_ip.reserve_floating_ip(name=self.fake_floating_ip['name'], 
                 target='target')
        print(response)
        self.assertEqual(response['name'], self.fake_floating_ip['name'])
 
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', common.fake_create)
    def test_reserve_floating_ip_not_working(self):
        """Test reserve_floating_ip should not work."""
        response = self.floating_ip.reserve_floating_ip(name=self.fake_floating_ip['name'],
                target='target')
        self.assertNotEqual(response['id'], self.fake_floating_ip['name'])
       
