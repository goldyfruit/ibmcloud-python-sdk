from ibmcloud_python_sdk.resource import resource_group
import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.key import Key

# import tests.Common as common

from tests.Key import Key as key
from tests.Common import Common

class KeyTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             key.authentication)
        self.patcher.start()
        self.key = Key()

    def tearDown(self):
        self.patcher.stop()

# get_keys
    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    def test_get_keys(self):
        """Test get_keys."""
        response = self.key.get_keys()
        self.assertNotEqual(len(response["keys"]), 0)

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.return_exception)
    def test_get_keys_with_exception(self):
        """Test get_keys (error by exception)."""
        with self.assertRaises(Exception):
            self.key.get_keys()
# get_key
    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    def test_get_keys_with_name(self):
        """Test get_key (with name)"""
        response = self.key.get_key(key.name)
        self.assertEqual(response['name'], key.name)

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    @patch.object(Key, 'get_keys', key.return_not_found)
    def test_get_keys_error_name_not_found(self):
        """Test get_key (name not found)"""
        response = self.key.get_key(key.name)
        self.assertEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    @patch.object(Key, 'get_keys', key.get_keys_return_error)
    def test_get_keys_error_unpredictable_A(self):
        """Test get_key (unpredictable error (name))"""
        response = self.key.get_key(key.name)
        self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    # @patch.object(Key, 'get_keys', key.return_not_found)
    def test_get_keys_with_id(self):
        """Test get_key (by id))"""
        response = self.key.get_key(key.id)
        print(response)
        self.assertEqual(response["id"], key.id)

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    @patch.object(Key, 'get_keys', key.return_not_found)
    @patch.object(Key, 'get_key_by_id', key.return_error)
    def test_get_keys_error_by_id(self):
        """Test get_key (error by id)"""
        response = self.key.get_key(key.id)
        self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    @patch.object(Key, 'get_keys', key.return_exception)
    def test_get_keys_error_by_exception(self):
        """Test get_key (error by exception)"""
        with self.assertRaises(Exception):
            self.key.get_key(key.name)

# get_key_by_id
    @patch('ibmcloud_python_sdk.vpc.key.qw', key.return_exception)
    # @patch.object(Key, 'get_keys', key.return_exception)
    def test_get_keys_error_by_exception(self):
        """Test get_key (error by exception)"""
        with self.assertRaises(Exception):
            self.key.get_key_by_id(key.id)

# create_key
    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw_with_payload)
    def test_create_key(self):
        """Test create_key."""
        response = self.key.create_key(name=key.name,
                                        public_key='public_key')
        self.assertEqual(response['name'], key.name)

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw_with_payload)
    @patch('ibmcloud_python_sdk.resource.resource_group.qw', key.get_resource_group)
    def test_create_key_with_payload(self):
        """Test create_key (with payload)."""
        response = self.key.create_key(name=key.name,
                                        public_key="public_key",
                                        resource_group="my-resource-group",
                                        type="rsa")
        self.assertEqual(response['name'], key.name)

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw_with_payload)
    @patch('ibmcloud_python_sdk.resource.resource_group.qw', Common.return_not_found)
    def test_create_key_with_rg_not_found(self):
        """Test create_key (rg not found)."""
        response = self.key.create_key(name=key.name,
                                        public_key="public_key",
                                        resource_group="my-resource-group",
                                        type="rsa")

        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.return_exception_with_payload)
    @patch('ibmcloud_python_sdk.resource.resource_group.qw', key.get_resource_group)
    def test_create_key_error_by_exception(self):
        """Test create_key (error by exception)."""
        with self.assertRaises(Exception):
            response = self.key.create_key(name=key.name,
                                        public_key="public_key",
                                        resource_group="my-resource-group",
                                        type="rsa")
# delete_key

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    def test_delete_key(self):
        """Test delete_key."""
        response = self.key.delete_key(key.name)
        print(response)
        self.assertEqual(response["status"], "deleted")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw_404_on_delete)
    def test_delete_key_return_404(self):
        """Test delete_key (with 404 error)."""
        response = self.key.delete_key(key.name)
        print(response)
        self.assertEqual(response, "Forbiden")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    @patch.object(Key, 'get_keys', key.return_not_found)
    def test_delete_key_error_by_key(self):
        """Test delete_key (error key_not_found)."""
        response = self.key.delete_key(key.name)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.key.qw', key.return_exception)
    @patch.object(Key, 'get_keys', key.return_not_found)
    def test_delete_key_error_by_exception(self):
        """Test delete_key (error by exception)."""
        with self.assertRaises(Exception):
            response = self.key.delete_key(key.name)

    # @patch('ibmcloud_python_sdk.vpc.key.qw', key.qw)
    # def test_get_key_with_name(self):
    #     """Test get_key with name as parameter."""
    #     response = self.key.get_key(self.fake_key['name'])
    #     print(response)
    #     self.assertEqual(response['name'], self.fake_key['name'])

