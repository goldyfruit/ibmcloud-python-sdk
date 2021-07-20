import unittest

from mock import patch

from ibmcloud_python_sdk.resource.resource_instance import ResourceInstance
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup as ResourceGroup

from tests.ResourceInstance import ResourceInstance as resource_instance
from tests.Common import Common

class ResourceInstanceTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             resource_instance.authentication)
        self.patcher.start()
        self.ri = ResourceInstance()

    def tearDown(self):
        self.patcher.stop()

# create_resource_instance
    @patch('ibmcloud_python_sdk.resource.resource_instance.qw',
        resource_instance.qw_5_args)
    @patch.object(ResourceGroup, 'get_resource_group',
        resource_instance.get_resource_group)
    def test_create_resource_instance(self):
        """Test create_resource_instance."""
        response = self.ri.create_resource_instance(
            name=resource_instance.name,
            resource_group="my-rg",
            resource_plan="my-plan",
            tags="tag1",
            allow_cleanup="yes",
            parameters="my-parameters",
            target="my-target")
        self.assertEqual(response["resources"][0]["name"], resource_instance.name)

    @patch('ibmcloud_python_sdk.resource.resource_instance.qw',
        resource_instance.qw_5_args)
    @patch.object(ResourceGroup, 'get_resource_group',
        resource_instance.return_exception)
    def test_create_resource_instance_error_by_exception(self):
        """Test create_resource_instance (error by exception)."""
        with self.assertRaises(Exception):
            response = self.ri.create_resource_instance(
                name=resource_instance.name,
                resource_group="my-rg",
                resource_plan="my-plan",
                tags="tag1",
                allow_cleanup="yes",
                parameters="my-parameters",
                target="my-target")

# get_resource_instances


# get_resource_instance

# get_resource_instance_by_guid

# get_resource_instance_by_name

# delete_resource_instance

