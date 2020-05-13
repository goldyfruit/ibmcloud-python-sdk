import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.power import get_power_headers as headers


class Image():

    def __init__(self):
        self.cfg = params()

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
        :return Image information
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
