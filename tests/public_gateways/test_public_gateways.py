from ibmcloud_python_sdk.vpc import floating_ip
import unittest

from mock import patch

# import ibmcloud_python_sdk.config
from ibmcloud_python_sdk.vpc.gateway import Gateway as Gateway
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup as ResourceGroup
from ibmcloud_python_sdk.vpc.floating_ip import Fip as FloatingIP
from ibmcloud_python_sdk.vpc.vpc import Vpc as Vpc

import tests.common as common

from tests.common import PublicGateway as pgw
from tests.common import Common as Common

class GatewayTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             pgw.authentication)
        self.patcher.start()
        self.gateway = Gateway()



    def tearDown(self):
        self.patcher.stop()

# get_public_gateways
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    def test_get_gateways(self):
        """Test get_gateways ."""
        response = self.gateway.get_public_gateways()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.return_exception)
    def test_get_gateways_error_by_exception(self):
        """Test get_gateways (return exception)."""
        with self.assertRaises(Exception):
            response = self.gateway.get_public_gateways()

# get_public_gateway

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    def test_get_gateway_with_name(self):
       """Test get_public_gateway_with_name."""
       response = self.gateway.get_public_gateway(pgw.name)
       self.assertEqual(response['name'], pgw.name)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    @patch.object(Gateway, 'get_public_gateway_by_name', pgw.return_error)
    def test_get_gateway_with_name(self):
       """Test get_public_gateway_with_id (with error)."""
       response = self.gateway.get_public_gateway(pgw.name)
       self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    def test_get_gateway_with_id(self):
       """Test get_public_gateway_with_id."""
       response = self.gateway.get_public_gateway(pgw.id)
       self.assertEqual(response['id'], pgw.id)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    @patch.object(Gateway, 'get_public_gateway_by_id', pgw.return_error)
    def test_get_gateway_with_id(self):
       """Test get_public_gateway_with_id (with error)."""
       response = self.gateway.get_public_gateway(pgw.id)
       self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    @patch.object(Gateway, 'get_public_gateway_by_name', pgw.return_error)
    def test_get_gateway_by_name_with_error(self):
        """Test get_public_gateway_by_name (with error)."""
        response = self.gateway.get_public_gateway_by_name(pgw.name)
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.return_exception)
    def test_get_gateway_with_name_error_by_exception(self):
        """Test get_public_gateway_with_name (with exception)."""
        with self.assertRaises(Exception):
            response = self.gateway.get_public_gateway(pgw.name)


# get_public_gateway_by_id
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    def test_get_gateway_by_id(self):
       """Test get_public_gateway_by_id as parameter."""
       response = self.gateway.get_public_gateway_by_id(pgw.id)
       self.assertEqual(response['name'], pgw.name)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw)
    @patch.object(Gateway, 'get_public_gateway_by_id', pgw.return_error)
    def test_get_gateway_by_id_with_error(self):
        """Test get_public_gateway_by_id (with error)."""
        response = self.gateway.get_public_gateway_by_id(pgw.id)
        self.assertEqual(response['errors'][0]['code'], 'unpredictable_error')

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.return_exception)
    def test_get_gateway_by_id_with_exception(self):
        """Test get_public_gateway_by_id (with exception)."""
        with self.assertRaises(Exception):
            response = self.gateway.get_public_gateway_by_id(pgw.id)

# create_public_gateway
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.create)
    @patch.object(ResourceGroup, 'get_resource_group', pgw.get_resource_group)
    @patch.object(FloatingIP, 'get_floating_ip', pgw.get_floating_ip)
    @patch.object(Vpc, 'get_vpc', pgw.get_vpc)
    def test_create_gateway(self):
        """Test create_public_gateway."""
        response = self.gateway.create_public_gateway(
            name="my-name",
            resource_group=pgw.resource_group_id,
            floating_ip="my",
            vpc="my-vpc",
            zone="my-zone"
        )
        self.assertEqual(response['id'], pgw.id)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', Common.qw)
    @patch.object(ResourceGroup, 'get_resource_group', pgw.return_not_found)
    def test_create_gateway_with_rg_not_found(self):
        """Test create_public_gateway (with not_found on resource group)."""
        response = self.gateway.create_public_gateway(
            name="my-name",
            resource_group=pgw.resource_group_id,
            floating_ip="my",
            vpc="my-vpc",
            zone="my-zone"
        )
        self.assertEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', Common.qw)
    @patch.object(ResourceGroup, 'get_resource_group', pgw.get_resource_group)
    @patch.object(FloatingIP, 'get_floating_ip', pgw.return_not_found)
    def test_create_gateway_with_fp_not_found(self):
        """Test create_public_gateway (with not_found on floating ip)."""
        response = self.gateway.create_public_gateway(
            name="my-name",
            resource_group=pgw.resource_group_id,
            floating_ip="my",
            vpc="my-vpc",
            zone="my-zone"
        )
        self.assertEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.create)
    @patch.object(ResourceGroup, 'get_resource_group', pgw.get_resource_group)
    @patch.object(FloatingIP, 'get_floating_ip', pgw.get_floating_ip)
    @patch.object(Vpc, 'get_vpc', pgw.return_not_found)
    def test_create_gateway_with_vpc_not_found(self):
        """Test create_public_gateway (with vpc not_found)."""
        response = self.gateway.create_public_gateway(
            name="my-name",
            resource_group=pgw.resource_group_id,
            floating_ip="my",
            vpc="my-vpc",
            zone="my-zone"
        )
        self.assertEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.return_exception)
    def test_get_gateway_with_name(self):
        """Test get_create_public_gateway (with exception)."""
        with self.assertRaises(Exception):
            self.gateway.create_public_gateway(
                vpc="my-vpc",
                zone="my-zone"
            )

# get_public_gateway_by_id
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', Common.qw)
    def test_get_gateway_with_name(self):
       """Test get_public_gateway_by_id."""
       response = self.gateway.get_public_gateway_by_id(pgw.id)
       print(response['id'])
       self.assertEqual(response['id'], pgw.id)

# delete_public_gateway
    @patch('ibmcloud_python_sdk.vpc.gateway.qw', Common.qw)
    def test_delete_public_gateway(self):
        """Test delete_public_gateway."""
        response = self.gateway.delete_public_gateway(pgw.name)
        print("*****")
        print(response)
        self.assertEqual(response["status"], 'deleted')

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.qw_404_on_delete)
    def test_delete_public_gateway_with_error(self):
        """Test delete_public_gateway (with error)."""
        response = self.gateway.delete_public_gateway(pgw.name)
        self.assertEqual(response, 'Forbiden')

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', pgw.return_exception)
    def test_delete_public_gateway_with_exception(self):
        """Test delete_public_gateway (with exception)."""
        with self.assertRaises(Exception):
            self.gateway.delete_public_gateway(pgw.id)

    @patch('ibmcloud_python_sdk.vpc.gateway.qw', Common.return_not_found)
    def test_delete_public_gateway_with_not_found(self):
        """Test delete_public_gateway (with not_found)."""
        response = self.gateway.delete_public_gateway(pgw.name)
        self.assertNotEqual(response['errors'], "")