import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup

import tests.common as common


class ResourceTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             common.fake_auth)
        self.patcher.start()
        self.resource = ResourceGroup()
        self.fake_resource = {}
        self.fake_resource['name'] = 'sdk'
        self.fake_resource['id'] = '0737_b06fd819-66d6-4802-ab51-f23061d981dd'
        self.fake_resource['default_security_group'] = 'fruit-average-shaping\
                                                        -gone-denture-rumor'
        self.fake_resource['default_network_acl'] = 'unpainted-crucial-trimmer-\
                                                    perennial-zipfile-barcode'

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', common.fake_get_call)
    def test_get_resources(self):
        """Test get_resources ."""
        response = self.resource.get_resource_groups()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', common.fake_get_call)
    def test_get_resource_with_name(self):
        """Test get_resource with name as parameter."""
        response = self.resource.get_resource_groups_by_account(
            self.fake_resource['name'])
        print(response)
        self.assertEqual(response['resource_groups'][0]['name'],
                         self.fake_resource['name'])
