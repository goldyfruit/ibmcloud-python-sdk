import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Dns():

    def __init__(self):
        self.cfg = params()
        self.resource_group_id = "aef66560191746fe804b9a66874f62b1"
        self.resource_plan_id = "dc1460a6-37bd-4e2b-8180-d0f86ff39baa"

    def get_resource_instances(self):
        """
        Retrieve all dns instances
        """
        result = []
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances")

            resource_instances = qw("rg", "GET", path, headers())
            for resource_instance in resource_instances["data"]["resources"]:
                if resource_instance["resource_plan_id"] == self.resource_plan_id : 
                    result.append(resource_instance)
            # Return data
            return result
        except Exception as error:
            print("Error fetching resource instances. {}").format(error)
            raise


    # Get specific resource instance by ID or by name
    # This method is generic and should be used as prefered choice
    def get_resource_instance(self, resource_instance):
        by_name = self.get_resource_instance_by_name(resource_instance)
        if "errors" in by_name:
            print(by_name)
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_guid = self.get_resource_instance_by_guid(resource_instance)
                    if "errors" in by_guid:
                        return by_guid
                    return by_guid
                else:
                    return by_name
        else:
            return by_name


    # Get specific resource instance by GUID
    def get_resource_instance_by_guid(self, guid):
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances/{}").format(guid)
            resource_instance = qw("rg", "GET", path, headers())["data"]
        
            # Test if the resource instance is for DNS operation
            if resource_instance["resource_plan_id"] == self.resource_plan_id:
                return resource_instance
            else:
                return ({"errors": [{"code": "not_found",
                    "msg": "The instance is not suitable for DNS operations"}]
                    })
        except Exception as error:
            print("Error fetching resource resource instance. {}").format(error)
            raise


    # Get specific resource instance by name
    def get_resource_instance_by_name(self, name):
        resource_instances = self.get_resource_instances()

        for resource_instance in resource_instances:
            if resource_instance["name"] == name and \
                resource_instance["resource_plan_id"] == self.resource_plan_id:
                    return resource_instance
            else:
                return ({"errors": [{"code": "not_found", 
                    "msg": "No instance suitable for DNS operations found."}]
                    })



    # Create DNS zone
    def create_zone(self, **kwargs):
        # Required parameters
        required_args = set(["name", "resource_instance"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'description': kwargs.get('description'),
            'label': kwargs.get('label'),
        }

        # Construct payload
        payload = {}

        for key, value in args.items():
             payload[key] = value
            
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("dns", "POST", path, headers(),
                    json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating instance. {error}")
            raise


    def get_zones(self):
        """
        Retrieve all zones
        """
        try:
            # Connect to api endpoint for vpcs
            path = ("")

            # Return data
            return qw("dns", "GET", path, headers())
        except Exception as error:
            print("Error fetching dns zones. {}").format(error)
            raise

    def test(self):
        print(self.cfg)
