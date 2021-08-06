import os
import json
import re
from unittest import TestCase
from mock import patch
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup
from tests.constants import ID_REGEXP
from tests.common import get_headers, read_one, qw, qw_not_found, \
    qw_exception, qw_api_error, qw_delete_code_204, qw_delete_code_400


class ResourceGroupTestCase(TestCase):
    def setUp(self):
        self.type = 'resource_groups'
        self.content = read_one('resource_group/resource_groups.json', 'resources')
        self.quota = read_one('resource_group/quotas.json', 'resources')
        self.resource_group = ResourceGroup()
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', get_headers)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


    def get_quotas(path, index=0):
        """This function returns a generated JSON token.
        """
        is_id = re.findall(ID_REGEXP, path)
        data_file = f'{os.path.dirname(__file__)}/quotas.json'
        with open(data_file, 'r') as json_file:
            try:
                if is_id:
                    return {'data': json.load(json_file)['resources'][index]}
                return {'data': json.load(json_file)}
            except json.JSONDecodeError as err:
                return err

    def qw_quotas(arg1, arg2, path, headers=None, payload=None):
        """This function is used to mock the query_wrapper function from
        utils/common. It returns information collected from get_all()
        function.
        """
        return ResourceGroupTestCase.get_quotas(path)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_resource_groups(self):
        response = self.resource_group.get_resource_groups()
        self.assertEqual(len(response['resources']), 2)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_default_resource_group(self):
        response = self.resource_group.get_default_resource_group()
        self.assertTrue(response['default'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_resource_group_by_id(self):
        response = self.resource_group.get_resource_group_by_id(
            self.content['id'])
        self.assertEqual(response['id'], self.content['id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_resource_group_by_name(self):
        response = self.resource_group.get_resource_group_by_name(
            self.content['name'])
        self.assertEqual(response['name'], self.content['name'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_resource_group_with_id(self):
        response = self.resource_group.get_resource_group(
            self.content['id'])
        self.assertEqual(response['id'], self.content['id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw)
    def test_get_resource_group_with_name(self):
        response = self.resource_group.get_resource_group(self.content['name'])
        self.assertEqual(response['name'], self.content['name'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_not_found)
    def test_get_default_resource_group_not_found(self):
        response = self.resource_group.get_default_resource_group()
        self.assertEqual(response['errors'][0]['code'], 'not_found')


    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_exception)
    def test_get_resource_groups_exception(self):
        with self.assertRaises(Exception):
            self.resource_group.get_resource_groups()

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_exception)
    def test_get_quota_definitions_exception(self):
        with self.assertRaises(Exception):
            self.resource_group.get_quota_definitions()

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_exception)
    def test_get_quota_definition_exception(self):
        with self.assertRaises(Exception):
            self.resource_group.get_quota_definition(self.quota['_id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_exception)
    def test_get_resource_group_by_id_exception(self):
        with self.assertRaises(Exception):
            self.resource_group.get_resource_group_by_id(self.content['id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_exception)
    def test_get_resource_group_by_name_exception(self):
        with self.assertRaises(Exception):
            self.resource_group.get_resource_group_by_name(self.content['name'])


    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_quotas)
    def test_get_quota_definitions(self):
        response = self.resource_group.get_quota_definitions()
        self.assertEqual(len(response['resources']), 12)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_quotas)
    def test_get_quota_definition_by_id(self):
        response = self.resource_group.get_quota_definition_by_id(self.quota['_id'])
        self.assertEqual(response['_id'], self.quota['_id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_quotas)
    def test_get_quota_definition_by_name(self):
        response = self.resource_group.get_quota_definition_by_name(self.quota['name'])
        self.assertEqual(response['name'], self.quota['name'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_quotas)
    def test_get_quota_definition_with_id(self):
        response = self.resource_group.get_quota_definition(self.quota['_id'])
        self.assertEqual(response['_id'], self.quota['_id'])

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', qw_quotas)
    def test_get_quota_definition_with_name(self):
        response = self.resource_group.get_quota_definition(self.quota['name'])
        self.assertEqual(response['name'], self.quota['name'])
