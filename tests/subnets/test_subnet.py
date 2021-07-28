import unittest

from mock import patch
from ibmcloud_python_sdk.vpc.subnet import Subnet
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup
from ibmcloud_python_sdk.vpc.vpc import Vpc as Vpc

from tests.Subnet import Subnet as subnet


class SubnetTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             subnet.authentication)
        self.patcher.start()
        self.subnet = Subnet()

    def tearDown(self):
        self.patcher.stop()

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnets(self):
        """Test get_subnets."""
        response = self.subnet.get_subnets()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnets_false(self):
        """Test get_subnets should not work."""
        response = self.subnet.get_subnets()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnet_with_name(self):
        """Test get_subnet with name as parameter."""
        response = self.subnet.get_subnet(subnet.name)
        self.assertEqual(response['name'], subnet.name)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnet_with_id(self):
        """Test get_subnet with id as parameter."""
        response = self.subnet.get_subnet(subnet.id)
        self.assertEqual(response['id'], subnet.id)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    @patch.object(Subnet, 'get_subnet_by_name', subnet.return_error)
    def test_get_subnet_error_by_name(self):
        """Test get_subnet (error by_name)."""
        response = self.subnet.get_subnet("10.0.0.1")
        self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    @patch.object(Subnet, 'get_subnet_by_id', subnet.return_error)
    def test_get_subnet_error_by_id(self):
        """Test get_subnet (error by_id)."""
        response = self.subnet.get_subnet("121345")
        self.assertNotEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.return_not_found)
    def test_get_subnet_with_error(self):
        """Test get_subnet_with_id (not_found)."""
        response = self.subnet.get_subnet("random name")
        self.assertNotEqual(len(response['errors']), 0)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnet_by_id(self):
        """Test get_subnet_with_id as parameter."""
        response = self.subnet.get_subnet_by_id(subnet.id)
        self.assertEqual(response['id'], subnet.id)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnet_network_acl(self):
        """Test get_subnet_network_acl as parameter."""
        response = self.subnet.get_subnet_network_acl(subnet.id)
        self.assertEqual(response['id'], subnet.id)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.qw)
    def test_get_subnet_public_gateway(self):
        """Test get_subnet_public_gateway as parameter."""
        response = self.subnet.get_subnet_public_gateway(subnet.id)
        self.assertEqual(response['id'], subnet.id)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.return_exception)
    def test_get_subnets_error_by_exception(self):
        """Test get_subnets should not work."""
        with self.assertRaises(Exception):
            self.subnet.get_subnets()

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.return_exception)
    def test_get_subnet_by_id_error_by_exception(self):
        """Test get_subnet_by_id (error by exception)."""
        with self.assertRaises(Exception):
            self.subnet.get_subnet_by_id(subnet.id)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.return_exception)
    def test_get_subnet_network_acl_error_by_exception(self):
        """Test get_subnet_network_acl (error by exception)."""
        with self.assertRaises(Exception):
            self.subnet.get_subnet_network_acl(subnet.name)

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.return_exception)
    def test_get_subnet_public_gateway_error_by_exception(self):
        """Test get_subnet_ublic_gatewa (error by exception)."""
        with self.assertRaises(Exception):
            self.subnet.get_subnet_public_gateway(subnet.name)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw',
           subnet.qw_with_payload)
    @patch.object(ResourceGroup, 'get_resource_group',
                  subnet.subnet_return_not_found)
    @patch.object(Vpc, 'get_vpc', subnet.get_vpc)
    def test_create_subnet_rg_return_error(self):
        """Test create_subnet (rg return error)."""
        response = self.subnet.create_subnet(
            name="my-name",
            total_ipv4_address_count=256,
            resource_group=subnet.resource_group_id,
            zone='us-south-1',
            vpc="my-vpc")
        self.assertEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.subnet.qw', subnet.create)
    @patch.object(ResourceGroup, 'get_resource_group',
                  subnet.get_resource_group)
    @patch.object(Vpc, 'get_vpc', subnet.get_vpc)
    def test_create_subnet(self):
        """Test create_subnet."""
        response = self.subnet.create_subnet(
            name="my-name",
            total_ipv4_address_count=256,
            resource_group=subnet.resource_group_id,
            zone="my-zone",
            vpc="my-vpc")
        self.assertEqual(response["id"], subnet.id)

# create_subnet
# attach_network_acl
# attach_public_gateway
# detach_public_gateway
# delete_su
