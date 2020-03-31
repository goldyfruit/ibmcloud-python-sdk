import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.instance import Instance

from .. import common as common
from . import test_instance_fake_url as instance

class VPCTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.instance = Instance()
        self.fake_instance = {}
        self.fake_instance['name'] = 'sdk'
        self.fake_instance['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_instance['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_instance['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_get_call)
    def test_get_instances(self):
        """Test get_instances ."""
        response = self.instance.get_instances()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_get_call)
    def test_get_instance_with_name(self):
        """Test get_instance with name as parameter."""
        response = self.instance.get_instance(self.fake_instance['name'])
        self.assertEqual(response['name'], self.fake_instance['name'])

## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.instance.instance.qw', common.fake_get_one)
##    def test_get_instance_with_id(self):
##        """Test get_instance with id as parameter."""
##        response = self.instance.get_instance(self.fake_instance['id'])
##        self.assertEqual(response['id'], self.fake_instance['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_get_one)
#    def test_get_instance_default_security_group(self):
#        """Test get_instance_default_security_group."""
#        response = self.instance.get_instance_default_security_group(self.fake_instance['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_instance['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_get_one)
#    def test_get_instance_default_network_acl(self):
#        """Test get_instance_default_network_acl."""
#        response = self.instance.get_instance_default_network_acl(self.fake_instance['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_instance['default_network_acl'])
#
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.fake_create_instance)
    def test_create_instance_working(self):
        """Test create_instance should work."""
        response = self.instance.create_instance(name=self.fake_instance['name'], 
                pni_subnet='subnet', 
                image='image', 
                profile='profile', 
                zone='zone')
        self.assertEqual(response['name'], self.fake_instance['name'])
 
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.fake_create_instance)
    def test_create_instance_not_working(self):
        """Test create_instance should not work."""
        response = self.instance.create_instance(name=self.fake_instance['name'],
                 pni_subnet='subnet', 
                image='image', 
                profile='profile', 
                zone='zone')
        self.assertNotEqual(response['id'], self.fake_instance['name'])
       
