import json
from . import config as ic

class Image():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn = self.cfg.conn

    # Get all Image
    def get_images(self):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching images. {error}")
            raise


    # Get specific Image by ID
    def get_image_by_id(self, id):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching Image with ID {id}. {error}")
            raise

    # Get specific Image by name
    def get_image_by_name(self, name):
        try:
            # Connect to api endpoint for images
            path = ("/v1/images/?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Loop over instance until filter match
            for image in json.loads(data)['images']:
                if image['name'] == name:
                    # Return response data
                    return image

            # Return response if no Image is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching Image with name {name}. {error}")
            raise

    # Create Image
    def create_image(self, **kwargs):
        # Required parameters
        required_args = set(["name", "resource_group"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                payload["resource_group"] = {"id": args["resource_group"]}
            if key == "file":
                payload["file"] = {"id": args["file"]}
            if key == "operating_system":
                payload["operating_system"] = {"name": args["operating_system"]}
            else:
                payload[key] = value
        try:
            # Connect to api endpoint for images
            path = ("/v1/images?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("POST", path, json.dumps(payload), self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error creating Image. {error}")
            raise
