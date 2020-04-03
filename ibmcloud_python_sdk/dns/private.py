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
                        "message": "No resource instance found"}]
                        })
            # Test if the resource instance is for DNS operation
            if resource_instance["resource_plan_id"] == self.resource_plan_id:
                return resource_instance
            else:
                return ({"errors": [{"code": "not_found",
                    "message": "The resource instance is not suitable for DNS operations"}]
                    })
        except Exception as error:
            print("Error fetching resource resource instance. {}").format(error)
            raise


    # Get specific resource instance by name
    def get_resource_instance_by_name(self, name):
        resource_instances = self.get_resource_instances()

        if len(resource_instances) == 0:
            return ({"errors": [{"code": "not_found",
                "message": "No resource instance suitable for DNS operations found."}]})
        
        if "errors" in resource_instances:
            return resource_instances

        for resource_instance in resource_instances:
            if resource_instance["name"] == name and \
                resource_instance["resource_plan_id"] == self.resource_plan_id:
                    return resource_instance
            else:
                return ({"errors": [{"code": "not_found", 
                    "message": "No resource instance suitable for DNS operations found."}]
                    })


    # Get specific dns zone id
    def get_dns_zone_by_name(self, **kwargs):
        # Required parameters
        required_args = ['name', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # Construct payload
        try:
            resource_instance_guid = self.get_resource_instance(args['resource_instance'])["guid"]
        except Exception as error:
            print(f"Unable to find resource instance : {error}.")
            raise

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)
            
            dns_zones = qw("dns", "GET", path, headers())["data"]

            if "error" in dns_zones or len(dns_zones) == 0:
                return ({"error": [{"status_code": 404,
                    "message": "No dns zone found."}]})
           
            # Find the existing domain matching the query
            for dns_zone in dns_zones['dnszones']:
                if dns_zone["name"] == args['name']:
                    return dns_zone
            # Return error message if no existing domain matches the query
            return ({"error": [{"status_code": 404, 
                "message": "No dns zone found."}]})

        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise


    # Lookup function to get dns zone id and resource instance id
    def get_dns_zone_and_resource_instance_id(self, dns_zone, resource_instance):
        # Get resource instane GUID
        try:
            ri = self.get_resource_instance(resource_instance)
            resource_instance_guid = ri['guid']
        except Exception as error:
            print(f"Error getting resource instace guid. {error}")
            raise
        
        # Get Zone id
        try:
            zone = self.get_dns_zone_by_name(name=dns_zone, 
                    resource_instance=resource_instance)
            zone_id = zone['id']
        except Exception as error:
            print(f"Error getting resource instace guid. {error}")
            raise
        
        return(zone_id, resource_instance_guid)
 

    # Create DNS zone
    def create_zone(self, **kwargs):
        # Required parameters
        required_args = set(["name", "resource_instance"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'description': kwargs.get('description') or "",
            'label': kwargs.get('label') or "",
        }
        resource_instance = kwargs.get('resource_instance')
        
        payload = {}

        try:
            ri = self.get_resource_instance(resource_instance)
            resource_instance_guid = ri["guid"]
        except Exception as error:
            print(f"Error getting resource instace guid. {error}")
            raise

        # Construct payload
        for key, value in args.items():
            payload[key] = value

        try:
            # Connect to api endpoint for dns zone
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)
            # Return data
            return qw("dns", "POST", path, headers(),
                    json.dumps(payload))["data"]
        
        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise

    # Add permitted network to dns zone's acls
    def add_permitted_network(self, **kwargs):
        """
        Add permitted network to dns zone

        :param name: required. The unique user-defined name for this ima.

        :param resource_group: Optional. The resource group to use.
        
        :param resource_instance: required. The name of the dns resource instance
        
        :param vpc_crn: required. The allowed VPC'CRN : crn:v1:staging:public:is:us-east ....
        """
        # Required parameters
        required_args = set(["name", "resource_instance", "vpc_crn"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'vpc_crn': kwargs.get('vpc_crn'),
            'resource_instance': kwargs.get('resource_instance'),
        }
        #resource_instance = kwargs.get('resource_instance')
        
        payload = {}

        # Get zone ID and resource instane GUID
        zone_id, resource_instance_guid = self.get_dns_zone_and_resource_instance_id(
                    args['name'], args['resource_instance'])

        # Construct payload
        payload["type"] = 'vpc'
        payload["permitted_network"] = {}
        payload["permitted_network"]["vpc_crn"] = args['vpc_crn']

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones/{}/permitted_networks").format(
                resource_instance_guid, zone_id)
            
            return qw("dns", "POST", path, headers(),
                    json.dumps(payload))["data"]

            #if "error" in acl:
            #    return ({"error": [{"status_code": 404,
            #        "message": "Add permitted nework failed."}]})
        
        except Exception as error:
            print(f"Error adding permitted network. {error}")
            raise

    def add_resource_record(self, **kwargs):
        """
        Add record in a specified zone

        :param name: required. The unique user-defined name for this ima.

        :param resource_instance: required. The name of the dns resource instance
        
        :param record: required. the record to add in the zone '{"name": "testB", "type": "A", "rdata": {"ip": "4.5.6.7"}}'

        """
        # Required parameters
        required_args = set(["name", "resource_instance", "record"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }
        
        # Get resource instane GUID
        try:
            ri = self.get_resource_instance(args['resource_instance'])
            resource_instance_guid = ri['guid']
        except Exception as error:
            print(f"Error getting resource instace guid. {error}")
            raise
        
        # Get Zone id
        try:
            zone = self.get_dns_zone_by_name(name=args['name'], 
                    resource_instance=args['resource_instance'])
            zone_id = zone['id']
        except Exception as error:
            print(f"Error getting resource instace guid. {error}")
            raise

        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones/{}/resource_records").format(
                resource_instance_guid, zone_id)
            
            return qw("dns", "POST", path, headers(),
                    json.dumps(args['record']))["data"]
       
        except Exception as error:
            print(f"Error adding resource record. {error}")
            raise


    def get_resource_records(self, **kwargs):
        """
        Add record in a specified zone

        :param name: required. The unique user-defined name for this ima.

        :param resource_instance: required. The name of the dns resource instance
        """
        # Required parameters
        required_args = set(["name", "resource_instance"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_instance': kwargs.get('resource_instance'),
        }
        
        # Get zone ID and resource instane GUID
        zone_id, resource_instance_guid = self.get_dns_zone_and_resource_instance_id(
                    args['name'], args['resource_instance'])
        try:
            # Connect to api endpoint for vpcs
            path = ("/v1/instances/{}/dnszones/{}/resource_records").format(
                resource_instance_guid, zone_id)
            
            return qw("dns", "GET", path, headers())["data"]
       
        except Exception as error:
            print(f"Error adding permitted network. {error}")
            raise


    def delete_resource_record(self, **kwargs):
        """
        Dlete record in a specified zone

        :param name: required. The unique user-defined name for this ima.

        :param record: required. The dns record name to delete.

        :param resource_instance: required. The name of the dns resource instance.

        """
        # Required parameters
        required_args = set(["name", "record", "resource_instance"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }
        
        # Get zone ID and resource instane GUID
        zone_id, resource_instance_guid = self.get_dns_zone_and_resource_instance_id(
                    args['name'], args['resource_instance'])

        # Get all records 
        records = self.get_resource_records(name=args['name'], 
                resource_instance=args['resource_instance'])
 
        for record in records['resource_records']:
            print(record['name'])
            if record['name'] ==  args['record']:
                try:
                    # Connect to api endpoint for vpcs
                    path = ("/v1/instances/{}/dnszones/{}/resource_records/{}").format(
                    resource_instance_guid, zone_id, record['id'])
            
                    return qw("dns", "DELETE", path, headers())["data"]
       
                except Exception as error:
                    print(f"Error adding permitted network. {error}")
                    raise

        else:
            return ({"errors": [{"code": "not_found",
                "message": "No dns record found"}] })
