import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found

from ibmcloud_python_sdk.utils.common import check_args

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
        
            if "status_code" in resource_instance:
                if resource_instance["status_code"] == 404:
                    return ({"errors": [{"code": "not_found",
                        "msg": "No resource instance found"}]
                        })
            # Test if the resource instance is for DNS operation
            if resource_instance["resource_plan_id"] == self.resource_plan_id:
                return resource_instance
            else:
                return ({"errors": [{"code": "not_found",
                    "msg": "The resource instance is not suitable for DNS operations"}]
                    })
        except Exception as error:
            print("Error fetching resource resource instance. {}").format(error)
            raise


    # Get specific resource instance by name
    def get_resource_instance_by_name(self, name):
        resource_instances = self.get_resource_instances()

        if len(resource_instances) == 0:
            return ({"errors": [{"code": "not_found",
                "msg": "No resource instance suitable for DNS operations found."}]})
        
        if "errors" in resource_instances:
            return resource_instances

        for resource_instance in resource_instances:
            if resource_instance["name"] == name and \
                resource_instance["resource_plan_id"] == self.resource_plan_id:
                    return resource_instance
            else:
                return ({"errors": [{"code": "not_found", 
                    "msg": "No resource instance suitable for DNS operations found."}]
                    })


    # Get specific dns zone id
    def get_dns_zone_info(self, **kwargs):
        # Required parameters
        required_args = ['name', 'resource_instance']
        #check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # Construct payload
        try:
            resource_instance_guid = self.get_resource_instance(args['resource_instance'])["guid"]
        except Exception as error:
            print(f"Unable to find resource instance : {args['resource_instance']}.")
            raise

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones").format(
                resouce_instance_guid)

            dns_zones = qw("dns", "GET", path, headers(),
                    json.dumps(payload))["data"]

            if "error" in dns_zones or len(dns_zones) == 0:
                return ({"error": [{"status_code": 404,
                    "msg": "No dns zone found."}]})
            
            for dns_zone in dns_zones["data"]:
                if dns_zone["name"] == name:
                    return dns_zone
                else:
                    return ({"error": [{"status_code": 404, 
                        "msg": "No dns zone found."}]})
            # Return data

        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise


    # Create DNS zone
    def create_zone(self, **kwargs):
        # Required parameters
        required_args = set(["name", "resource_instance"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'description': kwargs.get('description'),
            'label': kwargs.get('label'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # Construct payload
        payload = {}

        resource_instance_guid = self.get_resource_instance(resource_instance)["guid"]
        for key, value in args.items():
             payload[key] = value
        
                     
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones").format(
                resouce_instance_guid)

            # Return data
            return qw("dns", "POST", path, headers(),
                    json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating dns zone. {error}")
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
