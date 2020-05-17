import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.power import instance


class Image():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_images(self):
        """Retrieve image list

        :return: List of images
        :rtype: dict
        """
        try:
            # Connect to api endpoint for images
            path = ("/pcloud/v1/images")

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching images. {}".format(error))

    def get_image(self, image):
        """Retrieve specific image by name or by ID

        :param image: Image name or ID
        :return Image information
        :rtype dict
        """
        by_name = self.get_image_by_name(image)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_image_by_id(image)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_image_by_id(self, id):
        """Retrieve specific image by ID

        :param id: Image ID
        :return Image information
        :rtype dict
        """
        try:
            # Connect to api endpoint for images
            path = ("/pcloud/v1/images/{}".format(id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching image with ID {}. {}".format(id, error))

    def get_image_by_name(self, name):
        """Retrieve specific image by name

        :param image: Image name
        :return name information
        :rtype dict
        """
        try:
            # Retrieve images
            data = self.get_images()
            if "errors" in data:
                return data

            # Loop over images until filter match
            for image in data['images']:
                if image["name"] == name:
                    # Return data
                    return image

            # Return error if no image is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching image with name {}. {}".format(name, error))

    def get_instance_images(self, instance):
        """Retrieve images for a cloud instance

        :param instance: Cloud instance ID
        :return: List of images
        :rtype: dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for images
            path = ("/pcloud/v1/cloud-instances/{}/images".format(
                ci_info["name"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching images for cloud instance {}. {}".format(
                instance, error))

    def get_instance_image(self, instance, image):
        """Retrieve specific image by name or by ID for a cloud instance

        :param instance: Cloud instance ID
        :param image: Image name or ID
        :return Image information
        :rtype dict
        """
        by_name = self.get_instance_image_by_name(image)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_image_by_id(image)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_instance_image_by_id(self, instance, id):
        """Retrieve specific image by ID for a cloud instance

        :param instance: Cloud instance ID
        :param id: Image ID
        :return Image information
        :rtype dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/images/{}".format(
                ci_info["name"], id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching image with ID {} for cloud instance {}."
                  "{}".format(id, instance, error))

    def get_instance_image_by_name(self, instance, name):
        """Retrieve specific image by name

        :param instance: Cloud instance ID
        :param name: Image name
        :return Image information
        :rtype dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Retrieve images for a cloud instance
            data = self.get_instance_images(ci_info["name"])
            if "errors" in data:
                return data

            # Loop over images until filter match
            for image in data['images']:
                if image["name"] == name:
                    # Return data
                    return image

            # Return error if no image is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching image with name {} for cloud instance {}."
                  "{}".format(name, instance, error))

    def delete_instance_image(self, instance, image):
        """Delete cloud instance image

        :param instance: Cloud instance ID
        :param name: Image name
        :return Deletion status
        :rtype dict
        """
        try:
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if image exists and retrieve information
            image_info = self.get_instance_image(instance, image)
            if "errors" in image_info:
                return image_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/images/{}".format(
                instance, image))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting image {} from cloud instance {}. {}".format(
                image, instance, error))
