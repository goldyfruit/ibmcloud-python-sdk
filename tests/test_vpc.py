import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.vpc import Vpc

from . import config as tcfg

class VPCTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.config', tcfg.fake_apicall)
        self.patcher.start()
        self.vpc = Vpc()
        self.fake_vpc = {}
        self.fake_vpc['name'] = 'ansible-demo-vpc'
        self.fake_vpc['id'] = 'r006-74ff2772-9f3a-4263-bcaa-12fcffa3ed82'
        self.fake_vpc['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_vpc['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    def test_get_vpcs(self):
        """Test get_vpcs ."""
        response = self.vpc.get_vpcs()
        self.assertIn('vpcs', response)

    def test_get_vpc_with_name(self):
        """Test get_vpc with name as parameter."""
        response = self.vpc.get_vpc(self.fake_vpc['name'])
        self.assertEqual(response['name'], self.fake_vpc['name'])

    def test_get_vpc_with_id(self):
        """Test get_vpc with id as parameter."""
        response = self.vpc.get_vpc(self.fake_vpc['id'])
        self.assertEqual(response['id'], self.fake_vpc['id'])

    def test_get_vpc_default_security_group(self):
        """Test get_vpc_default_security_group."""
        response = self.vpc.get_vpc_default_security_group(self.fake_vpc['id'])
        self.assertEqual(response['name'], self.fake_vpc['default_security_group'])

    def test_get_vpc_default_network_acl(self):
        """Test get_vpc_default_network_acl."""
        response = self.vpc.get_vpc_default_network_acl(self.fake_vpc['id'])
        self.assertEqual(response['name'], self.fake_vpc['default_network_acl'])
 
    def test_create_vpc(self):
        """Test create_vpc."""
        print(self.patcher)
        response = self.vpc.create_vpc(name='test')
        #print(response['errors'])
        #help(response)
        #self.assertEqual(response['name'], self.fake_vpc['default_network_acl'])
        #self.assertEqual(1, 2)
        
