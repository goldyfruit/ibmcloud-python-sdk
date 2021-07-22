import unittest

from mock import patch
from ibmcloud_python_sdk.vpc.instance import Instance

from .Instance import Instance as instance
from tests.Common import Common


class InstanceTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             instance.authentication)
        self.patcher.start()
        self.instance = Instance()

    def tearDown(self):
        self.patcher.stop()

# get_instances
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instances(self):
        """Test get_instances."""
        response = self.instance.get_instances()
        self.assertNotEqual(len(response["instances"]), 0)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instances_error_by_exception(self):
        """Test get_instances (error by exception)."""
        with self.assertRaises(Exception):
            response = self.instance.get_instances()

# get_instance
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instance(self):
        """Test get_instance."""
        response = self.instance.get_instance(instance.name)
        self.assertNotEqual(len(response["name"]), instance.name)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_by_name', instance.return_not_found)
    def test_get_instance_error_by_name(self):
        """Test get_instance (error by name)."""
        response = self.instance.get_instance(instance.name)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_by_name', instance.return_error)
    def test_get_instance_by_name_return_error(self):
        """Test get_instance (by_name return error)."""
        response = self.instance.get_instance(instance.name)
        self.assertEqual(response["errors"][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_by_id', instance.return_not_found)
    def test_get_instance_error_by_id(self):
        """Test get_instance (error by id)."""
        response = self.instance.get_instance(instance.id)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instance_error_by_id(self):
        """Test get_instance (error by id)."""
        response = self.instance.get_instance(instance.id)
        self.assertEqual(response["id"], instance.id)

# get_instance_by_id
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instance_by_id(self):
        """Test get_instance_by_id."""
        response = self.instance.get_instance_by_id(instance.id)
        self.assertEqual(response["id"], instance.id)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_by_id_error_by_exception(self):
        """Test get_instance_by_id (error by exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_by_id(instance.id)

# get_instance_by_name
    @patch('ibmcloud_python_sdk.vpc.instance.qw', Common.return_not_found)
    def test_get_instance_by_name_error_by_name(self):
        """Test get_instance_by_name (error by name)."""
        response = self.instance.get_instance(instance.id)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_by_name_error_by_exception(self):
        """Test get_instance_by_name (error by exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_by_name(instance.name)

# get_instance_configuration
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instance_configuration(self):
        """Test get_instance_configuration."""
        response = self.instance.get_instance_configuration(instance.name)
        self.assertEqual(response["name"], instance.name)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', Common.return_not_found)
    @patch.object(Instance, 'get_instance_by_name', instance.return_not_found)
    def test_get_instance_configuration_error_by_name(self):
        """Test get_instance_configuration (error by name)."""
        response = self.instance.get_instance_configuration(instance.name)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', Common.return_not_found)
    @patch.object(Instance, 'get_instance_by_id', instance.return_not_found)
    def test_get_instance_configuration_error_by_name(self):
        """Test get_instance_configuration (error by id)."""
        response = self.instance.get_instance_configuration(instance.id)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_by_name', instance.return_not_found)
    def test_get_instance_configuration_with_id(self):
        """Test get_instance_configuration (with id)."""
        response = self.instance.get_instance_configuration(instance.id)
        self.assertEqual(response["id"], instance.id)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', Common.return_not_found)
    @patch.object(Instance, 'get_instance_by_name', instance.return_error)
    def test_get_instance_configuration_error_by_name(self):
        """Test get_instance_configuration (error by name)."""
        response = self.instance.get_instance_configuration(instance.name)
        self.assertEqual(response["errors"][0]["code"], "unpredictable_error")

    # TODO: to recheck
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_configuration_by_id', instance.return_not_found)
    @patch.object(Instance, 'get_instance_configuration_by_name', instance.return_not_found)
    def test_get_instance_configuration_error_by_name(self):
        """Test get_instance_configuration (error by id)."""
        response = self.instance.get_instance_configuration(instance.id)
        self.assertEqual(response["errors"][0]["code"], "not_found")

# get_instance_configuration_by_id
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_configuration_by_id_error_by_exception(self):
        """Test get_instance_configuration_by_id (error by exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_configuration_by_id(instance.id)


# get_instance_configuration_by_name
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_configuration_by_name_error_by_exception(self):
        """Test get_instance_configuration_by_name (error by exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_configuration_by_name(instance.name)

# get_instance_interfaces

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    def test_get_instance_interfaces(self):
        """Test get_instance_interfaces."""
        response = self.instance.get_instance_interfaces(instance.name)
        self.assertNotEqual(len(response["network_interfaces"]),0)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_interfaces_with_exception(self):
        """Test get_instance_interfaces (error by exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_interfaces(instance.name)

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_interfaces_by_name', instance.return_not_found)
    def test_get_instance_interfaces_by_name_by_name_not_found(self):
        """Test get_instance_interfaces (not found by name)."""
        response = self.instance.get_instance_interfaces(instance.name)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_interfaces_by_name', instance.return_error)
    def test_get_instance_interfaces_by_name_by_name_error(self):
        """Test get_instance_interfaces (error by name)."""
        response = self.instance.get_instance_interfaces(instance.name)
        self.assertEqual(response["errors"][0]["code"], "unpredictable_error")

    # TODO: to verify
    # @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    # @patch.object(Instance, 'get_instance_interfaces_by_id', instance.return_not_found)
    # def test_get_instance_interfaces_with_id_by_id_error(self):
    #     """Test get_instance_interfaces (error by id)."""
    #     response = self.instance.get_instance_interfaces(instance.id)
    #     print(response)
    #     self.assertEqual(response["errors"][0]["code"], "not_found")

    # TODO: to verify
    # @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    # @patch.object(Instance, 'get_instance_interfaces_by_id', instance.return_exception)
    # def test_get_instance_interfaces_by_error_by_exception(self):
    #     """Test get_instance_interfaces (error exception)."""
    #     # with self.assertRaises(Exception):
    #     response = self.instance.get_instance_interfaces(instance.id)
    #     # response = self.assertEqual(response["errors"][0]["code"], "not_found")
    #     print(response)
    #     self.assertEqual(0, 1)

# get_instance_interfaces_by_id
    # TODO: to verify lines 210, 211, 213
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_interfaces_by_id_error_by_exception(self):
        """Test get_instance_interfaces_by_id (error exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_interfaces(instance.id)
        # # response = self.assertEqual(response["errors"][0]["code"], "not_found")
        # print(response)
        # self.assertEqual(0, 1)


    # @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_get_call)
    # def test_get_instance_with_name(self):
    #     """Test get_instance with name as parameter."""
    #     response = self.instance.get_instance(self.fake_instance['name'])
    #     self.assertEqual(response['name'], self.fake_instance['name'])

# get_instance_interfaces_by_name
#   TODO: to verify
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.return_exception)
    def test_get_instance_interfaces_by_name_error_by_exception(self):
        """Test get_instance_interfaces_by_id (error exception)."""
        with self.assertRaises(Exception):
            self.instance.get_instance_interfaces_by_name(instance.id)

# get_instance_interface
    @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    @patch.object(Instance, 'get_instance_interface_by_name',
        instance.get_instance_interface_by_name)
    def test_get_instance_interface(self):
        """Test get_instance_interfaces_by_id (error exception)."""
        response = self.instance.get_instance_interface("my-instance",
            "my-interface")
        self.assertEqual(response["name"], instance.network_interface_name)

    # TODO: to verify
    # @patch('ibmcloud_python_sdk.vpc.instance.qw', instance.qw)
    # @patch.object(Instance, 'get_instance_interface_by_name',
    #     instance.return_not_found_2_args)
    # def test_get_instance_interface_with_by_name_not_found(self):
    #     """Test get_instance_interfaces_by_id (by name not found)."""
    #     response = self.instance.get_instance_interface("my-instance",
    #         "my-interface")
    #     print(response)
    #     self.assertEqual(response["errors"][0]["code"], "not_found")



    # @patch('ibmcloud_python_sdk.vpc.image.Image.get_image',
    #        custom.fake_get_image)
    # @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_create)
    # def test_create_instance_working(self):
    #     """Test create_instance should work."""
    #     response = self.instance.create_instance(
    #         name=self.fake_instance['name'],
    #         pni_subnet='subnet',
    #         image='image',
    #         profile='profile',
    #         zone='zone')
    #     self.assertEqual(response['name'], self.fake_instance['name'])

    # @patch('ibmcloud_python_sdk.vpc.image.Image.get_image',
    #        custom.fake_get_image)
    # @patch('ibmcloud_python_sdk.vpc.instance.qw', common.fake_create)
    # def test_create_instance_not_working(self):
    #     """Test create_instance should not work."""
    #     response = self.instance.create_instance(
    #         name=self.fake_instance['name'],
    #         pni_subnet='subnet',
    #         image='image',
    #         profile='profile',
    #         zone='zone')
    #     self.assertNotEqual(response['id'], self.fake_instance['name'])
