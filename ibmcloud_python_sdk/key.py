import json
from . import config as ic


class Key():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn = self.cfg.conn

    # Get all keys
    def get_keys(self):

        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching keys. {error}")
            raise

    # Get specific key by ID
    def get_key_by_id(self, id):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching key with ID {id}. {error}")
            raise

    # Get specific key by name
    def get_key_by_name(self, name):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Loop over keys until filter match
            for key in json.loads(data)['keys']:
                if key['name'] == name:
                    # Return response data
                    return key

            # Return response if no key is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching key with name {name}. {error}")
            raise

    # Create key
    def create_key(self, **kwargs):
        # Required parameters
        required_args = set(["name", "public_key", "resource_group"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'public_key': kwargs.get('public_key'),
            'resource_group': kwargs.get('resource_group'),
            'type': kwargs.get('type', 'rsa'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                payload["resource_group"] = {"id": args["resource_group"]}
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("POST", path, json.dumps(payload), self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error creating key. {error}")
            raise

    # Delete key
    def delete_key(self, id):
        try:
            # Connect to api endpoint for keys
            path = ("/v1/keys/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("DELETE", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()
            # res.status == 200 ou 404

        except Exception as error:
            print(f"Error deleting key with ID {id}. {error}")
            raise


