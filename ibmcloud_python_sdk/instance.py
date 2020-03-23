import http.client
import json
from . import config as ic


class Instance():

    def __init__(self):
        self.cfg = ic.Config()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers
        self.conn = self.cfg.conn

    # Get all instances
    def get_instances(self):

        try:
            # Connect to api endpoint for instances
            path = ("/v1/instances?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching instances. {error}")
            raise

    # Get specific instance by ID or by name
    # This method is generic and should be used as prefered choice
    def get_instance(self, instance):
        by_name = self.get_instance_by_name(instance)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_by_id(instance)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific instance by ID
    def get_instance_by_id(self, id):
        try:
            # Connect to api endpoint for instance
            path = ("/v1/instances/{}?version={}&generation={}").format(
                id, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching instance with ID {id}. {error}")
            raise

    # Get specific instance by name
    def get_instance_by_name(self, name):
        try:
            # Connect to api endpoint for instances
            path = ("/v1/instances/?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            for instance in json.loads(data)['instances']:
                if instance['name'] == name:
                    # Return response data
                    return instance

            # Return response if no instance is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching instance with name {name}. {error}")
            raise

    # Get all instance profiles
    def get_instance_profiles(self):
        try:
            # Connect to api endpoint for instance
            path = ("/v1/instance/profiles?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching instance profiles. {error}")
            raise

    # Get specific instance profile by name
    def get_instance_profile_by_name(self, name):
        try:
            # Connect to api endpoint for instance
            path = ("/v1/instance/profiles/{}?version={}"
                    "&generation={}").format(name, self.ver, self.gen)
            self.conn.request("GET", path, None, self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching instance profile with name {name}. {error}")
            raise

    # Create instance
    def create_instance(self, **kwargs):
        # Required parameters
        required_args = set(["image", "pni_subnet", "profile", "zone"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'keys': kwargs.get('keys'),
            'profile': kwargs.get('profile'),
            'resource_group': kwargs.get('resource_group'),
            'user_data': kwargs.get('user_data'),
            'vpc': kwargs.get('vpc'),
            'image': kwargs.get('image'),
            'pni_subnet': kwargs.get('pni_subnet'),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "profile":
                payload["profile"] = {"name": args["profile"]}
            elif key == "keys":
                if value is not None:
                    kp = []
                    for key_pair in args["keys"]:
                        tmp = {}
                        tmp["id"] = key_pair
                        kp.append(tmp)
                    payload["keys"] = kp
            elif key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "vpc":
                if value is not None:
                    payload["vpc"] = {"id": args["vpc"]}
            elif key == "image":
                payload["image"] = {"id": args["image"]}
            elif key == "pni_subnet":
                payload["primary_network_interface"] = {
                    "subnet": {"id": args["pni_subnet"]}}
            elif key == "zone":
                payload["zone"] = {"name": args["zone"]}
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances?version={}&generation={}").format(
                self.ver, self.gen)
            self.conn.request("POST", path, json.dumps(payload), self.headers)

            # Get and read response data
            res = self.conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error creating instance. {error}")
            raise
