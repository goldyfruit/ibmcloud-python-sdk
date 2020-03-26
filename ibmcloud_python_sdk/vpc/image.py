import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Image():

    def __init__(self):
        self.cfg = params()

    # Get operating systems
    def get_operating_systems(self):
        try:
            # Connect to api endpoint for operating_systems
            path = ("/v1/operating_systems?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching operating systems. {error}")
            raise

    # Get specific operating system
    def get_operating_system(self, name):
        try:
            # Connect to api endpoint for images
            path = ("/v1/operating_systems/{}?version={}"
                    "&generation={}").format(name, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching operating system with name {name}. {error}")
            raise

    # Get all images
    def get_images(self):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching images. {error}")
            raise

    # Get specific image by ID or by name
    # This method is generic and should be used as prefered choice
    def get_image(self, image):
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

    # Get specific image by ID
    def get_image_by_id(self, id):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching image with ID {id}. {error}")
            raise

    # Get specific image by name
    def get_image_by_name(self, name):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve images data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over images until filter match
            for image in data["images"]:
                if image["name"] == name:
                    # Return data
                    return image

            # Return error if no image is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching image with name {name}. {error}")
            raise

    # Create image
    def create_image(self, **kwargs):
        # Required parameters
        required_args = set(["file", "operating_system"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'file': kwargs.get('file'),
            'operating_system': kwargs.get('operating_system'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "file":
                payload["file"] = {"id": args["file"]}
            elif key == "operating_system":
                payload["operating_system"] = {
                    "name": args["operating_system"]}
            else:
                payload[key] = value
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating image. {error}")
            raise

    # Delete image
    # This method is generic and should be used as prefered choice
    def delete_image(self, image):
        by_name = self.delete_image_ip_by_name(image)
        if "errors" in by_name:
            for key_image in by_name["errors"]:
                if key_image["code"] == "not_found":
                    by_id = self.delete_image_ip_by_id(image)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete image by ID
    def delete_image_ip_by_id(self, id):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting image with ID {id}. {error}")
            raise

    # Delete image by name
    def delete_image_ip_by_name(self, name):
        try:
            # Check if image exists
            image = self.get_image_by_name(name)
            if "errors" in image:
                return image

            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}").format(
                image["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting image with name {name}. {error}")
            raise
