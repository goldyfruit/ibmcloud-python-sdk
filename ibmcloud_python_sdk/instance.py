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
