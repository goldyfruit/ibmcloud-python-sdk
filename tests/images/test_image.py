from ibmcloud_python_sdk.resource import resource_group
import unittest

from mock import patch

from ibmcloud_python_sdk.vpc.image import Image as Image
from ibmcloud_python_sdk.resource.resource_group import ResourceGroup as ResourceGroup
from ibmcloud_python_sdk.vpc.volume import Volume as Volume

from tests.Image import Image as image
from tests.Image import OperatingSystem as operating_system
# from tests.Common import Common
class ImageTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             image.authentication)
        self.patcher.start()
        self.image = Image()

    def tearDown(self):
        self.patcher.stop()

# get_operating_system
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    def test_get_operating_systems(self):
        """Test get_operating_systems."""
        response = self.image.get_operating_systems()
        self.assertNotEqual(len(response["operating_systems"]), 0)

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.return_exception)
    def test_get_operating_systems_error_by_exception(self):
        """Test get_operating_systems (error by_exception)."""
        with self.assertRaises(Exception):
            response = self.image.get_operating_systems()

    @patch('ibmcloud_python_sdk.vpc.image.qw', operating_system.qw)
    def test_get_operating_system(self):
        """Test get_operating_system (by_name)."""
        response = self.image.get_operating_system(operating_system.name)
        self.assertEqual(response["name"], operating_system.name)

    @patch('ibmcloud_python_sdk.vpc.image.qw', operating_system.return_exception)
    def test_get_operating_system_error_by_exception(self):
        """Test get_operating_system (error by_exception)."""
        with self.assertRaises(Exception):
            response = self.image.get_operating_system(operating_system.name)

# get_images
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    def test_get_images(self):
        """Test get_images."""
        response = self.image.get_images()
        self.assertNotEqual(len(response["images"]), 0)

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.return_exception)
    def test_get_images_error_by_exception(self):
        """Test get_images (error by exception)."""
        with self.assertRaises(Exception):
            response = self.image.get_images()

# get_image_by_name
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    def test_get_image_by_name(self):
        """Test get_image_by_name."""
        response = self.image.get_image_by_name(image.name)
        self.assertEqual(response['name'], image.name)

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_images', image.return_exception)
    def test_get_image_by_name_error_by_exception(self):
        """Test get_image_by_name (by_name return exception)."""
        with self.assertRaises(Exception):
            response = self.image.get_image_by_name(image.name)

    # @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    # @patch.object(Image, 'get_images', image.return_error)
    # def test_get_image_by_name_error_by_name(self):
    #     """Test get_image_by_name (error by_name)."""
    #     response = self.image.get_image_by_name(image.name)
    #     print(response)
    #     self.assertNotEqual(response['errors'][0]["code"], "not_found")


    # TODO: to verify
    # @patch('ibmcloud_python_sdk.vpc.image.qw', image.return_not_found)
    # def test_get_image_by_name_with_image_not_found(self):
    #     """Test get_image_by_name (with image not found)."""
    #     response = self.image.get_image_by_name(image.name)
    #     self.assertEqual(response["errors"][0]["code"], "not_found")

# get_image
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_name', image.return_not_found)
    def test_get_image_with_by_name_not_found(self):
        """Test get_image (by_name return not_found)."""
        response = self.image.get_image(image.name)
        print(response)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_name', image.return_error)
    def test_get_image_error_by_name(self):
        """Test get_image (error by_name)."""
        response = self.image.get_image(image.name)
        self.assertEqual(response["errors"][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_id', image.return_error)
    def test_get_image_error_by_id(self):
        """Test get_image (error by_id)."""
        response = self.image.get_image(image.id)
        self.assertEqual(response["errors"][0]["code"], "unpredictable_error")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_id', image.return_not_found)
    def test_get_image_with_by_id_not_found(self):
        """Test get_image (by_id return not_found)."""
        response = self.image.get_image(image.id)
        print(response)
        self.assertEqual(response["errors"][0]["code"], "not_found")

# get_image_by_id

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.return_exception)
    # @patch.object(Image, 'get_image_by_id', image.return_exception)
    def test_get_image_by_id_error_by_exception(self):
        """Test get_image_by_id (by_id return exception)."""
        with self.assertRaises(Exception):
            self.image.get_image_by_id(image.id)

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_id', image.return_error)
    def test_get_image_by_id_error_by_name(self):
        """Test get_image_by_id (error by_id)."""
        response = self.image.get_image_by_id(image.id)
        print(response)
        self.assertNotEqual(response['errors'][0]["code"], "not_found")

# create_image
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw_with_payload)
    @patch.object(ResourceGroup, 'get_resource_group', image.get_resource_group)
    @patch.object(Volume, 'get_volume', image.get_volume)
    def test_create_image(self):
        """Test create_image."""
        response = self.image.create_image(
            name=image.id,
            resource_group="my-resource-group",
            file="my-file",
            format="qcow2",
            source_volume="my-volume",
            operating_system="my-operating-system"
            )
        self.assertEqual(response["id"], image.id)

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw_with_payload_return_exception)
    @patch.object(ResourceGroup, 'get_resource_group', image.return_not_found)
    @patch.object(Volume, 'get_volume', image.get_volume)
    def test_create_image_error_rg_not_found(self):
        """Test create_image (error rg not found)."""
        response = self.image.create_image(
            name=image.id,
            resource_group="my-resource-group",
            file="my-file",
            format="qcow2",
            source_volume="my-volume",
            operating_system="my-operating-system"
            )
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw_with_payload)
    @patch.object(ResourceGroup, 'get_resource_group', image.get_resource_group)
    @patch.object(Volume, 'get_volume', image.return_not_found)
    def test_create_image_error_volume_not_found(self):
        """Test create_image (error volume not found)."""
        response = self.image.create_image(
            name=image.id,
            resource_group="my-resource-group",
            file="my-file",
            format="qcow2",
            source_volume="my-volume",
            operating_system="my-operating-system"
            )
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw_with_payload)
    @patch.object(ResourceGroup, 'get_resource_group', image.get_resource_group)
    @patch.object(Volume, 'get_volume', image.get_volume)
    def test_create_image_error_by_exception(self):
        """Test create_image (error by exception)."""
        response = self.image.create_image(
            name=image.id,
            resource_group="my-resource-group",
            file="my-file",
            format="qcow2",
            source_volume="my-volume",
            operating_system="my-operating-system"
            )
        with self.assertRaises(Exception):
            self.assertEqual(response["errors"][0]["code"], "not_found")

# delete_image
    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    def test_delete_image(self):
        """Test delete_image."""
        response = self.image.delete_image(image.name)
        self.assertEqual(response["status"], "deleted")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_name', image.return_not_found)
    def test_delete_image_error_by_image_not_found(self):
        """Test delete_image (error by image not found)."""
        response = self.image.delete_image(image.name)
        self.assertEqual(response["errors"][0]["code"], "not_found")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw_404_on_delete)
    def test_delete_image_with_404(self):
        """Test delete_image (with 404)."""
        response = self.image.delete_image(image.name)
        print(response)
        self.assertEqual(response, "Forbiden")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    def test_delete_image_with_(self):
        """Test delete_image (with 404)."""
        response = self.image.delete_image(image.name)
        print(response)
        self.assertEqual(response["status"], "deleted")

    @patch('ibmcloud_python_sdk.vpc.image.qw', image.qw)
    @patch.object(Image, 'get_image_by_name', image.return_exception)
    def test_get_image_by_name_error_by_exception(self):
        """Test get_image_by_name (by_name return exception)."""
        with self.assertRaises(Exception):
            response = self.image.delete_image(image.name)