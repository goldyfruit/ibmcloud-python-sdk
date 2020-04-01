import unittest

from mock import patch

import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.image import Image

import tests.common as common

class ImageTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
        self.patcher.start()
        self.image = Image()
        self.fake_image = {}
        self.fake_image['name'] = 'sdk'
        self.fake_image['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_image['default_security_group'] = 'fruit-average-shaping-gone-denture-rumor'
        self.fake_image['default_network_acl'] = 'unpainted-crucial-trimmer-perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_get_call)
    def test_get_images(self):
        """Test get_images ."""
        response = self.image.get_images()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_get_call)
    def test_get_image_with_name(self):
        """Test get_image with name as parameter."""
        response = self.image.get_image(self.fake_image['name'])
        print(response)
        self.assertEqual(response['name'], self.fake_image['name'])

## TODO: to verify
##    @patch('ibmcloud_python_sdk.auth.get_token', common.fake_auth)
##    @patch('ibmcloud_python_sdk.image.image.qw', common.fake_get_one)
##    def test_get_image_with_id(self):
##        """Test get_image with id as parameter."""
##        response = self.image.get_image(self.fake_image['id'])
##        self.assertEqual(response['id'], self.fake_image['id'])
#
#    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_get_one)
#    def test_get_image_default_security_group(self):
#        """Test get_image_default_security_group."""
#        response = self.image.get_image_default_security_group(self.fake_image['id'])
#        print(response)
#        self.assertEqual(response['default_security_group']['name'], self.fake_image['default_security_group'])
#
#    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_get_one)
#    def test_get_image_default_network_acl(self):
#        """Test get_image_default_network_acl."""
#        response = self.image.get_image_default_network_acl(self.fake_image['id'])
#        self.assertEqual(response['default_network_acl']['name'], self.fake_image['default_network_acl'])
#
    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_create)
    def test_create_image_working(self):
        """Test create_image should work."""
        response = self.image.create_image(name=self.fake_image['name'], 
                operating_system='operating_system=', 
                file='file')
        print(response)
        self.assertEqual(response['name'], self.fake_image['name'])
 
    @patch('ibmcloud_python_sdk.vpc.image.qw', common.fake_create)
    def test_create_image_not_working(self):
        """Test create_image should not work."""
        response = self.image.create_image(name=self.fake_image['name'],
                operating_system='operating_system=', 
                file='file')
        self.assertNotEqual(response['id'], self.fake_image['name'])
      
