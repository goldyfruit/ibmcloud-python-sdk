import unittest

from mock import patch

from ibmcloud_python_sdk.vpc.floating_ip import Fip

from tests.FloatingIp import FloatingIp as fip
class FloatingIPTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             fip.authentication)
        self.patcher.start()
        self.floating_ip = Fip()

    def tearDown(self):
        self.patcher.stop()

# get_floating_ips
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ips(self):
        """Test get_floating_ips."""
        response = self.floating_ip.get_floating_ips()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ips_false(self):
        """Test get_floating_ips should not work."""
        response = self.floating_ip.get_floating_ips()
        self.assertNotEqual(len(response), 0)

# get_floating_ip
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_with_name(self):
        """Test get_floating_ip with name as parameter."""
        response = self.floating_ip.get_floating_ip(fip.name)
        self.assertEqual(response['name'], fip.name)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_with_id(self):
        """Test get_floating_ip with id as parameter."""
        response = self.floating_ip.get_floating_ip(fip.id)
        self.assertEqual(response['id'], fip.id)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_with_address(self):
        """Test get_floating_ip (with_address)."""
        response = self.floating_ip.get_floating_ip(fip.address)
        self.assertEqual(response["address"], fip.address)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    @patch.object(Fip, 'get_floating_ip_by_name', fip.return_error)
    def test_get_floating_ip_error_by_name(self):
        """Test get_floating_ip (error by_name)."""
        response = self.floating_ip.get_floating_ip("10.0.0.1")
        self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    @patch.object(Fip, 'get_floating_ip_by_id', fip.return_error)
    def test_get_floating_ip_error_by_id(self):
        """Test get_floating_ip (error by_id)."""
        response = self.floating_ip.get_floating_ip("10.0.0.1")
        self.assertNotEqual(response['errors'][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    @patch.object(Fip, 'get_floating_ip_by_address', fip.return_error)
    def test_get_floating_ip_error_by_address(self):
        """Test get_floating_ip (error by_address)."""
        response = self.floating_ip.get_floating_ip("10.0.0.1")
        self.assertEqual(response['errors'][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_not_found)
    def test_get_floating_ip_with_error(self):
        """Test get_floating_ip_with_id (not_found)."""
        response = self.floating_ip.get_floating_ip("random name")
        self.assertNotEqual(len(response['errors']), 0)

    # get floating_ip_by_id
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_with_id(self):
        """Test get_floating_ip_with_id as parameter."""
        response = self.floating_ip.get_floating_ip_by_id(fip.id)
        self.assertEqual(response['id'], fip.id)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_not_found)
    def test_get_floating_ip_with_id_with_error(self):
        """Test get_floating_ip_with_id (with error)."""
        response = self.floating_ip.get_floating_ip_by_id(fip.id)
        self.assertNotEqual(len(response['errors']), 0)

    # get_floating_ip_by_name
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_by_name(self):
        """Test get_floating_ip_by_name."""
        response = self.floating_ip.get_floating_ip_by_name(fip.name)
        self.assertEqual(response['name'], fip.name)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_not_found)
    def test_get_floating_ip_by_name_error(self):
        """Test get_floating_ip_by_name (response in error) should work."""
        response = self.floating_ip.get_floating_ip_by_name(fip.name)
        self.assertNotEqual(len(response['errors']), 0)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_exception)
    def test_get_floating_ip_by_name_error_by_exception(self):
        """Test get_floating_ip_by_name (error by exception)."""
        with self.assertRaises(Exception):
            self.floating_ip.get_floating_ip_by_name(fip.name)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_exception)
    def test_get_floating_ip_by_id_error_by_exception(self):
        """Test get_floating_ip_by_id (error by exception)."""
        with self.assertRaises(Exception):
            self.floating_ip.get_floating_ip_by_id(fip.id)

    #  get_floating_ip_by_address
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_by_address(self):
        """Test get_floating_ip_by_address."""
        response = self.floating_ip.get_floating_ip_by_address(fip.address)
        self.assertEqual(response['address'], fip.address)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_not_found)
    def test_get_floating_ip_by_address_error_in_response(self):
        """Test get_floating_ip_by_address (return error)."""
        response = self.floating_ip.get_floating_ip_by_address(fip.address)
        self.assertNotEqual(response['errors'], "")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_get_floating_ip_by_address_no_resource_found(self):
        """Test get_floating_ip_by_address (no address found)."""
        response = self.floating_ip.get_floating_ip_by_address("10.10.10.1")
        print(response)
        self.assertNotEqual(response['errors'][0]['code'], "")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_exception)
    def test_get_floating_ip_by_address_error_by_exception(self):
        """Test get_floating_ip_by_address (error by exception)."""
        with self.assertRaises(Exception):
            self.floating_ip.get_floating_ip_by_address("10.10.10.1")

    # reserve_floating_ip
    @patch('ibmcloud_python_sdk.resource.resource_group.qw', fip.get_resource_group)
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.reserve_floating_ip)
    def test_reserve_floating_ip(self):
        """Test reserve_floating_ip."""
        response = self.floating_ip.reserve_floating_ip(
            name=fip.name,
            target='target',
            resource_group='Default',
            zone='us-south-1',
            payload="random payload")
        self.assertEqual(response['name'], fip.name)

    @patch('ibmcloud_python_sdk.resource.resource_group.qw', fip.get_resource_group)
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_exception)
    def test_reserve_floating_ip_error_by_execption(self):
        """Test reserve_floating_ip (error by exception)."""
        with self.assertRaises(Exception):
            self.floating_ip.reserve_floating_ip(
                name=fip.name,
                target='target',
                resource_group='Default',
                zone='us-south-1',
                payload="random payload")

    # TODO: check this function
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.create)
    def test_reserve_floating_ip(self):
        """Test reserve_floating_ip."""
        response = self.floating_ip.reserve_floating_ip(
            name=fip.name,
            target='target')
        print(response)
        self.assertEqual(response['name'], fip.name)

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_exception)
    def test_get_floating_ip_by_id_error_by_exeption(self):
        """Test get_floating_ip_by_id."""
        with self.assertRaises(Exception):
            self.floating_ip.get_floating_ip_by_id(fip.id)

    # TODO: release_floating_ip
    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.return_not_found)
    def test_release_floating_ip_error(self):
        """Test release_floating_ip (return error)."""
        response = self.floating_ip.release_floating_ip(
            "random_name")
        print(response)
        self.assertNotEqual(response['errors'], "")

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw)
    def test_release_floating_ip_with_204(self):
        """Test release_floating_ip (with 204)."""
        response = self.floating_ip.release_floating_ip(
            fip.name)
        self.assertEqual(response["status"], 'deleted')

    @patch('ibmcloud_python_sdk.vpc.floating_ip.qw', fip.qw_404_on_delete)
    def test_release_floating_ip_with_404(self):
        """Test release_floating_ip (with 404)."""
        response = self.floating_ip.release_floating_ip(
            fip.name)
        self.assertEqual(response, 'Forbiden')
