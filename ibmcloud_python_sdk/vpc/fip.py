import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Fip():

    def __init__(self):
        self.cfg = params()

    # Get all floating IPs
    def get_floating_ips(self):
        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching floating IPs. {error}")
            raise

    # Get specific floating IP by ID or by name
    # This method is generic and should be used as prefered choice
    def get_floating_ip(self, fip):
        by_name = self.get_floating_ip_by_name(fip)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_floating_ip_by_id(fip)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific floating IP by ID
    def get_floating_ip_by_id(self, id):
        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching floating IP with ID {id}. {error}")
            raise

    # Get specific floating IP by name
    def get_floating_ip_by_name(self, name):
        try:
            # Connect to api endpoint for instances
            path = ("/v1/floating_ips/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve floating IPs data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over instances until filter match
            for fip in data["floating_ips"]:
                if fip["name"] == name:
                    # Return data
                    return fip

            # Return error if no instance is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching floating IP with name {name}. {error}")
            raise

    # Reserve floating IP
    def reserve_floating_ip(self, **kwargs):
        # Required parameters
        required_args = set(["target"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'target': kwargs.get('target'),
            'resource_group': kwargs.get('resource_group'),
            'zone': kwargs.get('zone'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "target":
                payload["target"] = {"id": args["target"]}
            elif key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "zone":
                if value is not None:
                    payload["zone"] = {"name": args["zone"]}
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error reserving floating. {error}")
            raise

    # Delete floating IP
    # This method is generic and should be used as prefered choice
    def delete_floating_ip(self, fip):
        by_name = self.delete_floating_ip_by_name(fip)
        if "errors" in by_name:
            for key_fip in by_name["errors"]:
                if key_fip["code"] == "not_found":
                    by_id = self.delete_floating_ip_by_id(fip)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete floating IP by ID
    def delete_floating_ip_by_id(self, id):
        try:
            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting floating IP with ID {id}. {error}")
            raise

    # Delete floating IP by name
    def delete_floating_ip_by_name(self, name):
        try:
            # Check if floating IP exists
            fip = self.get_floating_ip_by_name(name)
            if "errors" in fip:
                return fip

            # Connect to api endpoint for floating_ips
            path = ("/v1/floating_ips/{}?version={}&generation={}").format(
                fip["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting floating IP with name {name}. {error}")
            raise
