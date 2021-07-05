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
        :rtype: list
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
            path = ("/pcloud/v1/images/{}".format(id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching image with ID {}. {}".format(id, error))

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
        :type instance: str
        :return: List of images per instance
        :rtype: list
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
        :type instance: str
        :param image: Image name or ID
        :type image: str
        :return: Image information
        :rtype: dict
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
        :type instance: str
        :param id: Image ID
        :type id: str
        :return: Image information
        :rtype: dict
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
        :type instance: str
        :param name: Image name
        :type name: str
        :return: Image information
        :rtype: dict
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

    def create_instance_image(self, **kwargs):
        """Create image for a cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param source: Source of the image
        :type source: str
        :param image_id: Image ID of existing source image
        :type image_id: str, optional
        :param name: Name to give created image
        :type name: str, optional
        :param region: Cloud Storage Region
        :type region: str, optional
        :param file: Cloud Storage image filename
        :type file: str, optional
        :param bucket: Cloud Storage bucket name
        :type bucket: str, optional
        :param access_key: Cloud Storage access key
        :type access_key: str, optional
        :param secret_key: Cloud Storage secret key
        :type secret_key: str, optional
        :param os_type: Image OS Type
        :type os_type: str, optional
        :param disk_type: Type of Disk
        :type disk_type: str, optional
        :return: Image information
        :rtype: dict
        """
        args = ["instance", "source"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('instance'),
            'source': kwargs.get('source'),
            'imageID': kwargs.get('image_id'),
            'imageName': kwargs.get('name'),
            'region': kwargs.get('region'),
            'imageFilename': kwargs.get('file'),
            'bucketName': kwargs.get('bucket'),
            'accessKey': kwargs.get('access_key'),
            'secretKey': kwargs.get('secret_key'),
            'osType': kwargs.get('os_type'),
            'diskType': kwargs.get('disk_type'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/images".format(
                ci_info["name"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating image for cloud instance {}. {}".format(
                args['instance'], error))

    def export_instance_image(self, **kwargs):
        """Export an image for a cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param image: Image ID of existing source image
        :type image: str
        :param region: Cloud Storage Region
        :type region: str, optional
        :param bucket: Cloud Storage bucket name
        :type bucket: str, optional
        :param access_key: Cloud Storage access key
        :type access_key: str, optional
        :param secret_key: Cloud Storage secret key
        :type secret_key: str, optional
        :return: Export image information
        :rtype: dict
        """
        args = ["instance", "image"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'instance': kwargs.get('source'),
            'image': kwargs.get('image'),
            'region': kwargs.get('region'),
            'bucketName': kwargs.get('bucket'),
            'accessKey': kwargs.get('access_key'),
            'secretKey': kwargs.get('secret_key'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "instance" and key != "image" and value is not None:
                payload[key] = value

        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(args['instance'])
            if "errors" in ci_info:
                return ci_info

            # Check if image exists and retrieve information
            image_info = self.get_instance_image(ci_info["name"],
                                                 args["image"])
            if "errors" in image_info:
                return image_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/images/{}/export".format(
                ci_info["name"], image_info["imageID"]))

            # Return data
            return qw("power", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error exporting image {} for cloud instance {}. {}".format(
                args['image'], args['instance'], error))

    def delete_instance_image(self, instance, image):
        """Delete cloud instance image

        :param instance: Cloud instance ID
        :type instance: str
        :param image: Image ID of existing source image
        :type image: str
        :return: Deletion status
        :rtype: dict
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
                ci_info["name"], image_info["imageID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting image {} from cloud instance {}. {}".format(
                image, instance, error))
