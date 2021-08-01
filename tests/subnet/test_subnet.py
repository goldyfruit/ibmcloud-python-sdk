from unittest import TestCase
from ibmcloud_python_sdk.vpc.subnet import Subnet
from mock import patch
from tests.common import get_headers, qw, qw_api_error, qw_not_found, \
    qw_exception, qw_api_error, get_one


class SubnetTestCase(TestCase):
    def setUp(self):
        self.type = 'subnets'
        self.content = get_one(self.type)
        self.subnet = Subnet()
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', get_headers)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnets(self):
        response = self.subnet.get_subnets()
        self.assertEqual(response['total_count'], 2)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_by_id(self):
        response = self.subnet.get_subnet_by_id(self.content['data']['id'])
        self.assertEqual(response['id'], self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_by_name(self):
        response = self.subnet.get_subnet_by_name(self.content['data']['name'])
        self.assertEqual(response['name'], self.content['data']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_with_id(self):
        response = self.subnet.get_subnet(self.content['data']['id'])
        self.assertEqual(response['id'], self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_with_name(self):
        response = self.subnet.get_subnet(self.content['data']['name'])
        self.assertEqual(response['name'], self.content['data']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_network_acl(self):
        response = self.subnet.get_subnet_network_acl(
            self.content['data']['id'])
        self.assertEqual(response['network_acl']['name'],
                         self.content['data']['network_acl']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    def test_get_subnet_public_gateway(self):
        response = self.subnet.get_subnet_public_gateway(
            self.content['data']['id'])
        self.assertEqual(response['public_gateway']['name'],
                         self.content['data']['public_gateway']['name'])

    # Not found
    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_not_found)
    def test_get_subnet_not_found(self):
        response = self.subnet.get_subnet('wrong_subnet_name')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_not_found)
    def test_get_subnet_network_acl_not_found(self):
        response = self.subnet.get_subnet_network_acl('wrong_subnet_name')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_not_found)
    def test_get_subnet_public_gateway_not_found(self):
        response = self.subnet.get_subnet_public_gateway('wrong_subnet_name')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    # API error
    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_api_error)
    def test_get_subnet_api_error(self):
        response = self.subnet.get_subnet(self.content['data']['id'])
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_api_error)
    def test_get_subnet_network_acl_api_error(self):
        response = self.subnet.get_subnet_network_acl(self.content['data']['id'])
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

    # Exception
    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    def test_get_subnets_exception(self):
        with self.assertRaises(Exception):
            self.subnet.get_subnets()

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    def test_get_subnet_by_id_exception(self):
        with self.assertRaises(Exception):
            self.subnet.get_subnet_by_id(self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    def test_get_subnet_by_name_exception(self):
        with self.assertRaises(Exception):
            self.subnet.get_subnet_by_name(self.content['data']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    def test_get_subnet_public_gateway_exception(self):
        with self.assertRaises(Exception):
            self.subnet.get_subnet_public_gateway(self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    def test_get_subnet_network_acl_exception(self):
        with self.assertRaises(Exception):
            self.subnet.get_subnet_network_acl(self.content['data']['id'])