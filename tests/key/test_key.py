import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.key import Key

from .. import common as common

class KeyTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.key = Key()
        self.fake_key = {}
        self.fake_key['name'] = 'sdk'
        self.fake_key['id'] = 'r006-84ddd169-031f-4732-9faa-aeef7c554df5'
        self.fake_key['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_key['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_get_call)
    def test_get_keys(self):
        """Test get_keys ."""
        response = self.key.get_keys()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_get_call)
    def test_get_key_with_name(self):
        """Test get_key with name as parameter."""
        response = self.key.get_key(self.fake_key['name'])
        print(response)
        self.assertEqual(response['name'], self.fake_key['name'])

## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.key.key.qw', common.fake_get_one)
##    def test_get_key_with_id(self):
##        """Test get_key with id as parameter."""
##        response = self.key.get_key(self.fake_key['id'])
##        self.assertEqual(response['id'], self.fake_key['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_get_one)
#    def test_get_key_default_security_group(self):
#        """Test get_key_default_security_group."""
#        response = self.key.get_key_default_security_group(self.fake_key['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_key['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_get_one)
#    def test_get_key_default_network_acl(self):
#        """Test get_key_default_network_acl."""
#        response = self.key.get_key_default_network_acl(self.fake_key['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_key['default_network_acl'])
#
    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_create)
    def test_create_key_working(self):
        """Test create_key should work."""
        response = self.key.create_key(name=self.fake_key['name'], 
                public_key='public_key')
        print(response)
        self.assertEqual(response['name'], self.fake_key['name'])
 
    @patch('ibmcloud_python_sdk.vpc.key.qw', common.fake_create)
    def test_create_key_not_working(self):
        """Test create_key should not work."""
        response = self.key.create_key(name=self.fake_key['name'],
                public_key='public_key')
        self.assertNotEqual(response['id'], self.fake_key['name'])
      
