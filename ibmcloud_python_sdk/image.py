import http.client
import json
from .config import conn, headers, version, generation


class Image():
    # Get all Image
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/Images/list_images
    # Doc: https://cloud.ibm.com/apidocs/vpc#list-all-images
    def get_images(self):
        try:
            # Connect to api endpoint for images
            path = f"/v1/images?version={version}&generation={generation}"
            conn.request("GET", path, None, headers)

            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching images. {error}")
            raise


    # Get specific Image by ID
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/Images/get_image
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-specified-image
    def get_image_by_id(self, id):
        try:
            # Connect to api endpoint for images
            path = f"/v1/images/{id}?version={version}&generation={generation}"
            conn.request("GET", path, None, headers)

            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching Image with ID {id}. {error}")
            raise

    # Get specific Image by name
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/Images/get_image
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-specified-image
    def get_image_by_name(self, name):
        try:
            # Connect to api endpoint for images
            path = f"/v1/images/?version={version}&generation={generation}"
            conn.request("GET", path, None, headers)

            # Get and read response data
            res = conn.getresponse()
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
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/Images/create_image
    # Doc: https://cloud.ibm.com/apidocs/vpc#create-a-image
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
            path = f"/v1/images?version={version}&generation={generation}"
            conn.request("POST", path, json.dumps(payload), headers)

            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error creating Image. {error}")
            raise
