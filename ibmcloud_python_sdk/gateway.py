import json
from . import config as ic_con
from . import common as ic_com


class Gateway():

    def __init__(self):
        self.cfg = ic_con.Config()
        self.common = ic_com.Common()
        self.ver = self.cfg.version
        self.gen = self.cfg.generation
        self.headers = self.cfg.headers

    # Get all public gateways
    def get_public_gateways(self):
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways?version={}&generation={}").format(
                self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching public gateways. {error}")
            raise

    # Get specific public gateway by ID or by name
    # This method is generic and should be used as prefered choice
    def get_public_gateway(self, gateway):
        by_name = self.get_public_gateway_by_name(gateway)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_public_gateway_by_id(gateway)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific public gateway by ID
    def get_public_gateway_by_id(self, id):
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/{}?version={}&generation={}").format(
                id, self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

        except Exception as error:
            print(f"Error fetching public gateway with ID {id}. {error}")
            raise

    # Get specific public gateway by name
    def get_public_gateway_by_name(self, name):
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/?version={}&generation={}").format(
                self.ver, self.gen)

            # Retrieve gateways data
            data = self.common.query_wrapper(
                "iaas", "GET", path, self.headers)["data"]

            # Loop over gateways until filter match
            for gateway in data["public_gateways"]:
                if gateway['name'] == name:
                    # Return response data
                    return gateway

            # Return error if no public gateway is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching public gateway with name {name}. {error}")
            raise

    # Create public gateway
    def create_public_gateway(self, **kwargs):
        # Required parameters
        required_args = set(["vpc", "zone"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'floating_ip': kwargs.get('floating_ip'),
            'vpc': kwargs.get('vpc'),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "floating_ip":
                if value is not None:
                    payload["floating_ip"] = {"address": args["floating_ip"]}
            elif key == "vpc":
                payload["vpc"] = {"id": args["vpc"]}
            elif key == "zone":
                payload["zone"] = {"name": args["zone"]}
            else:
                payload[key] = value
        print(payload)
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways?version={}&generation={}").format(
                self.ver, self.gen)

            # Return data
            return self.common.query_wrapper(
                "iaas", "POST", path, self.headers,
                json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating public gateway. {error}")
            raise

    # Delete public gateway
    # This method is generic and should be used as prefered choice
    def delete_public_gateway(self, gateway):
        by_name = self.delete_public_gateway_by_name(gateway)
        if "errors" in by_name:
            for key_gateway in by_name["errors"]:
                if key_gateway["code"] == "not_found":
                    by_id = self.delete_public_gateway_by_id(gateway)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete public gateway by ID
    def delete_public_gateway_by_id(self, id):
        try:
            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/{}?version={}&generation={}").format(
                id, self.ver, self.gen)

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting public gateway with ID {id}. {error}")
            raise

    # Delete public gateway by name
    def delete_public_gateway_by_name(self, name):
        try:
            # Check if public gateway exists
            gateway = self.get_public_gateway_by_name(name)
            if "errors" in gateway:
                return gateway

            # Connect to api endpoint for public_gateways
            path = ("/v1/public_gateways/{}?version={}&generation={}").format(
                gateway["id"], self.ver, self.gen)

            data = self.common.query_wrapper(
                "iaas", "DELETE", path, self.headers)

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting public gateway with name {name}. {error}")
            raise
