from unittest import TestCase
from mock import patch
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup
from ibmcloud_python_sdk.vpc.subnet import Subnet
from ibmcloud_python_sdk.vpc.vpc import Vpc
from ibmcloud_python_sdk.vpc.acl import Acl
from ibmcloud_python_sdk.vpc.gateway import Gateway
from tests.common import get_headers, get_one, qw, qw_not_found, qw_exception, \
    qw_api_error, qw_delete_code_204, qw_delete_code_400


class SubnetTestCase(TestCase):

    def setUp(self):
        self.type = 'subnets'
        self.content = get_one(self.type)
        self.subnet = Subnet()
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token', get_headers)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


    def get_subnet_network_acl(path, vpc):
        content = get_one('subnets')
        return {'id': content['data']['network_acl']['id']}

    def get_subnet_public_gateway(path, vpc):
        content = get_one('subnets')
        return {'id': content['data']['public_gateway']['id']}

    def get_resource_group(path, group):
        data = get_one('subnets')
        return {'id': data['data']['resource_group']['id']}

    def get_vpc(path, vpc):
        data = get_one('subnets')
        return {'id': data['data']['vpc']['id']}

    def get_subnet(path, vpc):
        data = get_one('subnets')
        return {'id': data['data']['id']}

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

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_api_error)
    def test_get_subnet_api_error(self):
        response = self.subnet.get_subnet(self.content['data']['id'])
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_api_error)
    def test_get_subnet_network_acl_api_error(self):
        response = self.subnet.get_subnet_network_acl(self.content['data']['id'])
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

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

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    @patch.object(Vpc, 'get_vpc', get_vpc)
    def test_create_subnet_exception(self):
        with self.assertRaises(Exception):
            self.subnet.create_subnet(vpc=self.content['data']['vpc']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    @patch.object(Acl, 'get_network_acl', get_subnet_network_acl)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_attach_network_acl_exception(self):
        with self.assertRaises(Exception):
            self.subnet.attach_network_acl(
                subnet=self.content['data']['id'],
                network_acl=self.content['data']['network_acl']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    @patch.object(Gateway, 'get_public_gateway', get_subnet_public_gateway)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_attach_public_gateway_exception(self):
        with self.assertRaises(Exception):
            self.subnet.attach_public_gateway(
                subnet=self.content['data']['id'],
                public_gateway=self.content['data']['public_gateway']['name'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_detach_public_gateway_exception(self):
        with self.assertRaises(Exception):
            self.subnet.detach_public_gateway(self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_exception)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_delete_subnet_exception(self):
        with self.assertRaises(Exception):
            self.subnet.delete_subnet(self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(ResourceGroup, 'get_resource_group', get_resource_group)
    @patch.object(Subnet, 'get_subnet_network_acl', get_subnet_network_acl)
    @patch.object(Subnet, 'get_subnet_public_gateway', get_subnet_public_gateway)
    @patch.object(Vpc, 'get_vpc', get_vpc)
    def test_create_subnet(self):
        response = self.subnet.create_subnet(
            name=self.content['data']['name'],
            total_ipv4_address_count=256,
            resource_group=self.content['data']['resource_group']['name'],
            network_acl=self.content['data']['network_acl']['name'],
            public_gateway=self.content['data']['public_gateway']['name'],
            routing_table=self.content['data']['routing_table']['name'],
            zone=self.content['data']['zone']['name'],
            vpc=self.content['data']['vpc']['name'])
        self.assertEqual(response['subnets'][0]['id'], self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(ResourceGroup, 'get_resource_group', qw_not_found)
    def test_create_subnet_resource_group_not_found(self):
        response = self.subnet.create_subnet(
            name=self.content['data']['name'],
            total_ipv4_address_count=256,
            resource_group='not_found',
            network_acl=self.content['data']['network_acl']['name'],
            public_gateway=self.content['data']['public_gateway']['name'],
            routing_table=self.content['data']['routing_table']['name'],
            zone=self.content['data']['zone']['name'],
            vpc=self.content['data']['vpc']['name'])
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(ResourceGroup, 'get_resource_group', get_resource_group)
    @patch.object(Subnet, 'get_subnet_network_acl', qw_not_found)
    @patch.object(Subnet, 'get_subnet_public_gateway', get_subnet_public_gateway)
    @patch.object(Vpc, 'get_vpc', get_vpc)
    def test_create_subnet_network_acl_not_found(self):
        response = self.subnet.create_subnet(
            name=self.content['data']['name'],
            total_ipv4_address_count=256,
            resource_group=self.content['data']['resource_group']['name'],
            network_acl='not_found',
            public_gateway=self.content['data']['public_gateway']['name'],
            routing_table=self.content['data']['routing_table']['name'],
            zone=self.content['data']['zone']['name'],
            vpc=self.content['data']['vpc']['name'])
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(ResourceGroup, 'get_resource_group', get_resource_group)
    @patch.object(Subnet, 'get_subnet_network_acl', get_subnet_network_acl)
    @patch.object(Subnet, 'get_subnet_public_gateway', qw_not_found)
    @patch.object(Vpc, 'get_vpc', get_vpc)
    def test_create_subnet_public_gateway_not_found(self):
        response = self.subnet.create_subnet(
            name=self.content['data']['name'],
            total_ipv4_address_count=256,
            resource_group=self.content['data']['resource_group']['name'],
            network_acl=self.content['data']['network_acl']['name'],
            public_gateway='not_found',
            routing_table=self.content['data']['routing_table']['name'],
            zone=self.content['data']['zone']['name'],
            vpc=self.content['data']['vpc']['name'])
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(ResourceGroup, 'get_resource_group', get_resource_group)
    @patch.object(Subnet, 'get_subnet_network_acl', get_subnet_network_acl)
    @patch.object(Subnet, 'get_subnet_public_gateway', get_subnet_public_gateway)
    @patch.object(Vpc, 'get_vpc', qw_not_found)
    def test_create_subnet_vpc_not_found(self):
        response = self.subnet.create_subnet(
            name=self.content['data']['name'],
            total_ipv4_address_count=256,
            resource_group=self.content['data']['resource_group']['name'],
            network_acl=self.content['data']['network_acl']['name'],
            public_gateway=self.content['data']['public_gateway']['name'],
            routing_table=self.content['data']['routing_table']['name'],
            zone=self.content['data']['zone']['name'],
            vpc='not_found')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Acl, 'get_network_acl', get_subnet_network_acl)
    def test_attach_network_acl(self):
        response = self.subnet.attach_network_acl(
            subnet=self.content['data']['name'],
            network_acl=self.content['data']['network_acl']['name'])
        self.assertEqual(response['id'], self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Acl, 'get_network_acl', qw_not_found)
    def test_attach_network_acl_not_found(self):
        response = self.subnet.attach_network_acl(
            subnet=self.content['data']['name'],
            network_acl='not_found')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Acl, 'get_network_acl', get_subnet_network_acl)
    @patch.object(Subnet, 'get_subnet', qw_not_found)
    def test_attach_network_acl_subnet_not_found(self):
        response = self.subnet.attach_network_acl(
            subnet='not_found',
            network_acl=self.content['data']['network_acl']['name'])
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Gateway, 'get_public_gateway', get_subnet_public_gateway)
    def test_attach_public_gateway(self):
        response = self.subnet.attach_public_gateway(
            subnet=self.content['data']['name'],
            public_gateway='my-public-gateway')
        self.assertEqual(response['id'], self.content['data']['id'])

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Gateway, 'get_public_gateway', qw_not_found)
    def test_attach_public_gateway_not_found(self):
        response = self.subnet.attach_public_gateway(
            subnet=self.content['data']['name'],
            public_gateway='not_found')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Gateway, 'get_public_gateway', get_subnet_public_gateway)
    @patch.object(Subnet, 'get_subnet', qw_not_found)
    def test_attach_public_gateway_subnet_not_found(self):
        response = self.subnet.attach_public_gateway(
            subnet='not_found',
            public_gateway=self.content['data']['public_gateway']['name'])
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_delete_code_204)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_detach_public_gateway(self):
        response = self.subnet.detach_public_gateway(
            self.content['data']['id'])
        self.assertEqual(response["status"], 'deleted')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Subnet, 'get_subnet', qw_not_found)
    def test_detach_public_gateway_not_found(self):
        response = self.subnet.detach_public_gateway('not_found')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_delete_code_400)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_detach_public_gateway_bad_request(self):
        response = self.subnet.detach_public_gateway(self.content['data']['id'])
        self.assertEqual(response, 'bad_request')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_delete_code_204)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_delete_subnet(self):
        response = self.subnet.delete_subnet(
            self.content['data']['id'])
        self.assertEqual(response["status"], 'deleted')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw)
    @patch.object(Subnet, 'get_subnet', qw_not_found)
    def test_delete_subnet_not_found(self):
        response = self.subnet.delete_subnet('not_found')
        self.assertEqual(response['errors'][0]['code'], 'not_found')

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', qw_delete_code_400)
    @patch.object(Subnet, 'get_subnet', get_subnet)
    def test_delete_subnet_bad_request(self):
        response = self.subnet.delete_subnet(self.content['data']['id'])
        self.assertEqual(response, 'bad_request')
