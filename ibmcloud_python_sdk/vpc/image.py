import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group
from ibmcloud_python_sdk.vpc import volume


class Image():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.ResourceGroup()
        self.volume = volume.Volume()

    def get_operating_systems(self):
        """Retrieve operating system list

        :return: List of operating systems
        :rtype: list
        """
        try:
            # Connect to api endpoint for operating_systems
            path = ("/v1/operating_systems?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching operating systems. {}".format(error))
            raise

    def get_operating_system(self, name):
        """Retrieve specific operating system

        :param name: Operating system name
        :type name: str
        :return: Operating system information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for operating_systems
            path = ("/v1/operating_systems/{}?version={}"
                    "&generation={}".format(name, self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching operating system {}. {}".format(name, error))
            raise

    def get_images(self):
        """Retrieve image list

        :return: List of images
        :rtype: list
        """
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching images. {}".format(error))
            raise

    def get_image(self, image):
        """Retrieve specific image

        :param image: Image name or ID
        :type image: str
        :return: Image information
        :rtype: dict
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
        :type id: str
        :return: Image information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching image with ID {}. {}".format(id, error))
            raise

    def get_image_by_name(self, name):
        """Retrieve specific image by name

        :param name: Image name
        :type name: str
        :return: Image information
        :rtype: dict
        """
        try:
            # Retrieve images
            data = self.get_images()
            if "errors" in data:
                return data

            # Loop over images until filter match
            for image in data["images"]:
                if image["name"] == name:
                    # Return data
                    return image

            # Return error if no image is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching image with name {}. {}".format(name, error))
            raise

    def create_image(self, **kwargs):
        """Create image

        :param name: The unique user-defined name for this image
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param file: The file from which to create the image
        :type file: str
        :param format: The format of the image and the image file
        :type format: str
        :param source_volume: The volume from which to create the image
        :type source_volume: str
        :param operating_system: The operating system included in this image
        :type operating_system: str
        :return: Image information
        :rtype: dict
        """
        args = ["file", "operating_system"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'file': kwargs.get('file'),
            'format': kwargs.get('format'),
            'source_volume': kwargs.get('source_volume'),
            'operating_system': kwargs.get('operating_system'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "file":
                    payload["file"] = {"href": args["file"]}
                elif key == "source_volume":
                    vol_info = self.volume.get_volume(args["source_volume"])
                    if "errors" in vol_info:
                        return vol_info
                    payload["source_volume"] = {"id": vol_info["id"]}
                elif key == "operating_system":
                    payload["operating_system"] = {
                        "name": args["operating_system"]}
                else:
                    payload[key] = value
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating image. {}".format(error))
            raise

    def delete_image(self, image):
        """Delete image

        :param image: Image name or ID
        :type image: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if image exists
            image_info = self.get_image_by_name(image)
            if "errors" in image_info:
                return image_info

            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}".format(
                image_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 202:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting image with name {}. {}".format(image, error))
            raise
