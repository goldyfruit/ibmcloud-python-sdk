import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk import resource_instance

from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.utils.common import check_args

class Dns():
    """Class implementing private DNS methods
    """

    def __init__(self):
        self.cfg = params()
        self.resource_instance = resource_instance.ResourceInstance()
        self.vpc = vpc.Vpc()
        # resource_group_id and self.resource_plan_id for free dns instance
        self.resource_group_id = "aef66560191746fe804b9a66874f62b1"
        self.resource_plan_id = "dc1460a6-37bd-4e2b-8180-d0f86ff39baa"

    # Get all dns zones
    def get_dns_zones(self, **kwargs):
        """Get all dns zone hosted by a resource instance

        :param resource_instance_guid: the GUID of the resource instance
        """
        # Required parameters
        required_args = ['resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        try:
            # Connect to api endpoint for dns zones
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)

            return qw("dns", "GET", path, headers())["data"]
        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise

    # Get specific dns zone by ID or by name
    # This method is generic and should be used as prefered choice
    def get_dns_zone(self, **kwargs):
        """Get a specific dns zone hosted by a resource instance

        param: dns_zone: the DNS zone name or id to query
        param: resource_instance: name or GUID of the resource instance
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

#        # get resource instance guid
#        ri = self.resource_instance.get_resource_instance(args['resource_instance'])
#        if "errors" in ri:
#            return ri
#        else:
#            resource_instance_guid = ri["guid"]

        by_name = self.get_dns_zone_by_name(dns_zone=args['dns_zone'],
                                            resource_instance=args['resource_instance'])
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_guid = self.get_dns_zone_by_id(dns_zone=args['dns_zone'],
                                                    resource_instance=args['resource_instance'])
                    if "errors" in by_guid:
                        return by_guid
                    return by_guid
                return by_name
        else:
            return by_name


    # Get specific dns zone by name
    def get_dns_zone_by_name(self, **kwargs):
        """Get dns zone by name

        :param: dns_zone: the DNS zone name to query
        :param: esource_instance_guid: name or GUID of the resource instance
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        try:
            # Connect to api endpoint for dns zones
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)

            dns_zones = qw("dns", "GET", path, headers())["data"]

            if "errors" in dns_zones or not dns_zones:
                return ({"errors": [{"code": "not_found",
                        "message": "No dns zones found."}]})

            # Find the existing domain matching the query
            for dns_zone in dns_zones['dnszones']:
                if dns_zone["name"] == args['dns_zone']:
                    return dns_zone

            # Return error message if no existing domain matches the query
            return ({"errors": [{"code": "not_found",
                    "message": "No dns zone found."}]})

        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise

    # Get specific dns zone by id
    def get_dns_zone_by_id(self, **kwargs):
        """Get DNS zone by id
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        try:
            # Connect to api endpoint for dns zones
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)

            dns_zones = qw("dns", "GET", path, headers())["data"]

            if "errors" in dns_zones or not dns_zones:
                return ({"errors": [{"code": "not_found",
                    "message": "No dns zone found."}]})

            # Find the existing domain matching the query
            for dns_zone in dns_zones['dnszones']:
                if dns_zone["id"] == args['dns_zone']:
                    return dns_zone
            # Return error message if no existing domain matches the query
            return ({"errors": [{"code": "not_found",
                "message": "No dns zone found."}]})

        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise



    # Lookup function to get dns zone id and resource instance
    def get_dns_zone_id(self, **kwargs):
        """Get DNS zone by ID
        """
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # Get Zone id
        try:
            zone = self.get_dns_zone_by_name(dns_zone=args['dns_zone'],
                    resource_instance=args['resource_instance'])
            if "errors" in zone:
                for key_name in zone["errors"]:
                    if key_name["code"] == "not_found":
                        return zone
            return zone['id']
        except Exception as error:
            print(f"Error getting dns zone id: {error}")
            raise


    # Create DNS zone
    def create_zone(self, **kwargs):
        """Create a zone in a specified resource instance

        :param: dns_zone: required. The user-defined name to create.
        :param: description: optional. A description for the domain.
        :param: label: optional: A label for the domain.
        :param: resource_instance: required. Name or guid of dns
            resource instance.
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'name': kwargs.get('dns_zone'),
            'description': kwargs.get('description') or "",
            'label': kwargs.get('label') or "",
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(kwargs.get('resource_instance'))
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        zone = self.get_dns_zone(
                    dns_zone=args['name'],
                    resource_instance=resource_instance_guid)

        if "errors" in zone:
            for key_zone in zone["errors"]:
                if key_zone["code"] == "not_found":
                    payload = {}

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
        return zone

    # Delete DNS zone
    def delete_zone(self, **kwargs):
        """Create a zone in a specified resource instance
        
        :param: dns_zone: required. The user-defined name to create.
        :param: resource_instance: required. Name or guid of dns
            resource instance.
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'name': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        dns_zone = self.get_dns_zone(dns_zone=args['name'],
                resource_instance=args['resource_instance'])

        if "errors" in dns_zone:
            return dns_zone
        dns_zone_id = dns_zone['id']

        try:
            # Connect to api endpoint for dns zone
            path = ("/v1/instances/{}/dnszones/{}").format(
                resource_instance_guid,
                dns_zone_id)

            # Return data
            result = qw("dns", "DELETE", path, headers())

            if result["data"] is None:
                if result["response"].getcode() == 204:
                    return({"message": "deletion request successfully initiated"})
            return result

        except Exception as error:
            print(f"Error creating dns zone. {error}")
            raise


    # Add permitted network to dns zone's acls
    def add_permitted_network(self, **kwargs):
        """Add permitted network to dns zone

        :param dns_zone: required. The user-defined name for this domain.
        :param resource_instance: required. Name or guid of dns resource
        instance.
        :param vpc: required. The allowed VPC name or id.
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance', 'vpc']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'vpc': kwargs.get('vpc'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # get vpc crn
        temp_vpc = self.vpc.get_vpc(args["vpc"])
        if "errors" in temp_vpc:
            return temp_vpc
        vpc_crn = temp_vpc["crn"]

        # Get zone ID
        zone_id = self.get_dns_zone_id(
                    dns_zone=args['dns_zone'],
                    resource_instance=resource_instance_guid)
        if "errors" in zone_id :
            return zone_id

        payload = {}

        # Construct payload
        payload["type"] = "vpc"
        payload["permitted_network"] = {}
        payload["permitted_network"]["vpc_crn"] = vpc_crn

        try:
            # Connect to api endpoint for permitted network
            path = ("/v1/instances/{}/dnszones/{}/permitted_networks").format(
                resource_instance_guid, zone_id)

            return qw("dns", "POST", path, headers(),
                    json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error adding permitted network. {error}")
            raise



    # Delete permitted network to dns zone's acls
    def delete_permitted_network(self, **kwargs):
        """Delete permitted network to dns zone

        :param dns_zone: required. The user-defined name for this domain.
        :param resource_instance: required. Name or guid of dns resource
        instance.
        :param vpc_crn: required. The allowed VPC's CRN :

        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance', 'vpc']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'vpc': kwargs.get('vpc'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # get vpc id
        temp_vpc = self.vpc.get_vpc(args["vpc"])
        if "errors" in temp_vpc:
            return temp_vpc
        vpc_id = temp_vpc["id"]

        # get zone ID
        zone_id = self.get_dns_zone_id(
                    dns_zone=args['dns_zone'],
                    resource_instance=resource_instance_guid,)
        if "errors" in zone_id:
            return zone_id

        # Construct payload
        try:
            # Connect to api endpoint for permitted network
            path = ("/v1/instances/{}/dnszones/{}/permitted_networks/{}").format(
                resource_instance_guid, zone_id, vpc_id)

            result = qw("dns", "DELETE", path, headers())
            if result["data"] is None:
                if result["response"].getcode() == 204:
                    return({"message": "deletion request successfully initiated"})
                return result
            return result
        except Exception as error:
            print(f"Error removing permitted network. {error}")
            raise


    def create_resource_record(self, **kwargs):
        """Add record in a specified zone

        :param name: required. The unique user-defined name for this ima.
        :param resource_instance: required. The name of the dns resource instance
        :param record: required. the record to add in the zone
            ex : '{ "name": "testB",
                    "type": "A",
                    "rdata": {
                        "ip": "4.5.6.7"
                     }
                  }'
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance', 'record']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # Get Zone id
        try:
            zone = self.get_dns_zone(dns_zone=args['dns_zone'],
                    resource_instance=args['resource_instance'])
            zone_id = zone['id']
        except Exception as error:
            print(f"Error getting zone id. {error}")
            raise

        try:
            # Connect to api endpoint for resource records
            path = ("/v1/instances/{}/dnszones/{}/resource_records").format(
                resource_instance_guid, zone_id)

            return qw("dns", "POST", path, headers(),
                    json.dumps(args['record']))["data"]

        except Exception as error:
            print(f"Error adding resource record. {error}")
            raise


    def get_resource_records(self, **kwargs):
        """Get record for a specified zone

        :param name: required. The unique user-defined name for this domain.
        :param resource_instance: required. The name of the dns resource instance
        """
        # Required parameters
        required_args = ['dns_zone', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # Get zone ID
        zone_id = self.get_dns_zone_id(
                    dns_zone=args['dns_zone'],
                    resource_instance=args['resource_instance'])
        try:
            # Connect to api endpoint for resource records
            path = ("/v1/instances/{}/dnszones/{}/resource_records").format(
                resource_instance_guid, zone_id)

            return qw("dns", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error getting resource records. {error}")
            raise


    def delete_resource_record(self, **kwargs):
        """Delete record in a specified zone

        :param name: required. The unique user-defined name for this ima.
        :param record: required. The dns record name to delete.
        :param resource_instance: required. Name or GUID of dns resource
            instance.
        """
        # Required parameters
        required_args = ['dns_zone', 'record', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # Get zone ID and resource instane GUID
        zone_id = self.get_dns_zone_id(
                    dns_zone=args["dns_zone"],
                    resource_instance=args["resource_instance"])

        # Get record ID
        record = self.get_resource_record(dns_zone=args["dns_zone"],
                resource_instance=args["resource_instance"],
                record=args["record"])
        if "errors" in record:
            return record
        record_id = record["id"]

        try:
            # Connect to api endpoint for resource records
            path = ("/v1/instances/{}/dnszones/{}/resource_records/{}").format(
                           resource_instance_guid,
                           zone_id, record_id)

            result = qw("dns", "DELETE", path, headers())["data"]
            if result is None:
                return({"message": "record successfully deleted"})
            return result

        except Exception as error:
                    print(f"Error deleting zone. {error}")
                    raise
        else:
            return ({"errors": [{"code": "not_found",
                "message": "No dns record found"}]})

    def get_resource_record(self, **kwargs):
        """Get resource records from a dns zone
        """
        # Required parameters
        required_args = ['dns_zone', 'record', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        by_name = self.get_resource_record_by_name(dns_zone=args['dns_zone'],
                 resource_instance=resource_instance_guid,
                 record_name=args['record'])

        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_resource_record_by_id(dns_zone=args['dns_zone'],
                            resource_instance=resource_instance_guid,
                            record_id=args['record'])
                    if "errors" in by_id:
                        return by_id
                    return by_id
                return by_name
        else:
            return by_name



    def get_resource_record_by_name(self, **kwargs):
        """Get record from a name

        :param  dns_zone:
        :param record_name:
        :param resource_instance
        """
        # Required parameters
        required_args = ['dns_zone', 'record_name', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record_name': kwargs.get('record_name'),
        }

        # get resource instance guid
        #ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        #if "errors" in ri:
        #    return ri
        #resource_instance_guid = ri["guid"]

        # Get list of records
        records = self.get_resource_records(\
                    dns_zone=args['dns_zone'],
                    resource_instance=args["resource_instance"])['resource_records']
        for record in records:
            if record['name'] == args['record_name']:
                return record
        return ({"errors": [{"code": "not_found",\
            "message": "No record found"}]})

    def get_resource_record_by_id(self, **kwargs):
        """Get record from an ID

        :param  dns_zone:
        :param record_id:
        :param resource_instance:
        """
        # Required parameters
        required_args = ['dns_zone', 'record_id', 'resource_instance']
        check_args(required_args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record_id': kwargs.get('record_id'),
        }

        # get resource instance guid
        #ri = self.resource_instance.get_resource_instance(args['resource_instance'])
        #if "errors" in ri:
        #    return ri
        #resource_instance_guid = ri["guid"]

        # Get zone ID and resource instane GUID
        records = self.get_resource_records(\
            dns_zone=args['dns_zone'],
            resource_instance=args["resource_instance"])['resource_records']

        for record in records:
            if record['id'] == args['record_id']:
                return record
        return ({"errors": [{"code": "not_found", "message": \
                "No record found"}]})
