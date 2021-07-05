import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.resource import resource_instance
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.utils.common import check_args


class Dns():

    def __init__(self):
        self.cfg = params()
        self.resource_instance = resource_instance.ResourceInstance()
        self.vpc = vpc.Vpc()
        # resource_group_id and self.resource_plan_id for free dns instance
        self.resource_group_id = "aef66560191746fe804b9a66874f62b1"
        self.resource_plan_id = "dc1460a6-37bd-4e2b-8180-d0f86ff39baa"

    def get_dns_zones(self, **kwargs):
        """Get all DNS zones hosted by a resource instance

        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: DNS zones
        :rtype: list
        """
        args = ['resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # Get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        try:
            # Connect to api endpoint for dns zones
            path = ("/v1/instances/{}/dnszones").format(
                resource_instance_guid)

            return qw("dns", "GET", path, headers())["data"]
        except Exception as error:
            print("Error creating dns zone. {}".format(error))
            raise

    def get_dns_zone(self, **kwargs):
        """Get a specific DNS zone hosted by a resource instance

        :param dns_zone: DNS zone name or ID to query
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: DNS zone information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }
        by_name = self.get_dns_zone_by_name(dns_zone=args['dns_zone'],
                                            resource_instance=args[
                                                'resource_instance'
                                            ])
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_guid = self.get_dns_zone_by_id(dns_zone=args[
                                                      'dns_zone'],
                                                      resource_instance=args[
                                                      'resource_instance'])
                    if "errors" in by_guid:
                        return by_guid
                    return by_guid
                return by_name
        else:
            return by_name

    def get_dns_zone_by_name(self, **kwargs):
        """Get DNS zone by name

        :param dns_zone: DNS zone name to query
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: DNS zone information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(args[
                                            'resource_instance'])
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
            print("Error creating dns zone. {}".format(error))
            raise

    def get_dns_zone_by_id(self, **kwargs):
        """Get DNS zone by id

        :param dns_zone: DNS zone ID to query
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: DNS zone information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance':  kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
                    args['resource_instance']
                )
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
            print("Error creating dns zone. {}".format(error))
            raise

    # DO WE NEED TO KEEP THIS FUNCTION?
    # def get_dns_zone_id(self, **kwargs):
    #     """Get DNS zone by ID

    #     :param dns_zone: the dns zone name.
    #     :param resource_instance: the associated resource instance.
    #     """
    #     required_args = ['dns_zone', 'resource_instance']
    #     check_args(required_args, **kwargs)

    #     # Set default value if required paramaters are not defined
    #     args = {
    #         'dns_zone': kwargs.get('dns_zone'),
    #         'resource_instance':  kwargs.get('resource_instance'),
    #     }

    #     # Get Zone id
    #     try:
    #         zone = self.get_dns_zone_by_name(dns_zone=args['dns_zone'],
    #                                          resource_instance=args[
    #                                              'resource_instance'])
    #         if "errors" in zone:
    #             for key_name in zone["errors"]:
    #                 if key_name["code"] == "not_found":
    #                     return zone
    #         return zone['id']
    #     except Exception as error:
    #         print("Error getting dns zone id: {}".format(error))
    #         raise

    def create_zone(self, **kwargs):
        """Create a zone in a specified resource instance

        :param dns_zone: The user-defined name to create
        :type dns_zone: str
        :param description: A description for the domain
        :type description: str, optional
        :param label: A label for the domain
        :type label: str, optional
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'name': kwargs.get('dns_zone'),
            'description': kwargs.get('description') or "",
            'label': kwargs.get('label') or "",
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(kwargs.get(
            'resource_instance'))
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
                        print("Error creating dns zone. {}".format(error))
                        raise
        return zone

    def delete_zone(self, **kwargs):
        """Delete a zone in from a specified resource instance

        :param dns_zone: DNS zone name to delete
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'name': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        dns_zone = self.get_dns_zone(dns_zone=args['name'],
                                     resource_instance=args[
                                         'resource_instance'])

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
                    return({"message":
                            "deletion request successfully initiated"})
            return result

        except Exception as error:
            print("Error creating dns zone. {}".format(error))
            raise

    def add_permitted_network(self, **kwargs):
        """Add permitted network to DNS zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :param vpc: The allowed VPC name or ID
        :type vpc: str
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance', 'vpc']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'vpc': kwargs.get('vpc'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
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
        if "errors" in zone_id:
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
            print("Error adding permitted network. {}".format(error))
            raise

    def delete_permitted_network(self, **kwargs):
        """Delete permitted network to dns zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :param vpc: The allowed VPC name or ID
        :type vpc: str
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance', 'vpc']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'vpc': kwargs.get('vpc'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance']
        )
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
            path = (
                "/v1/instances/{}/dnszones/{}/permitted_networks/{}").format(
                resource_instance_guid, zone_id, vpc_id)

            result = qw("dns", "DELETE", path, headers())
            if result["data"] is None:
                if result["response"].getcode() == 204:
                    return({"message":
                            "deletion request successfully initiated"})
                return result
            return result
        except Exception as error:
            print("Error removing permitted network. {}".format(error))
            raise

    def create_resource_record(self, **kwargs):
        """Add record in a specified zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :param record: The record to add in the zone, example:
            '{"name": "testB", "type": "A", "rdata": {"ip": "4.5.6.7"}}'
        :type record: dict
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance', 'record']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # Get Zone id
        try:
            zone = self.get_dns_zone(dns_zone=args['dns_zone'],
                                     resource_instance=args[
                                         'resource_instance'])
            zone_id = zone['id']
        except Exception as error:
            print("Error getting zone id. {}".format(error))
            raise

        try:
            # Connect to api endpoint for resource records
            path = ("/v1/instances/{}/dnszones/{}/resource_records").format(
                resource_instance_guid, zone_id)

            return qw("dns", "POST", path, headers(),
                      json.dumps(args['record']))["data"]

        except Exception as error:
            print("Error adding resource record. {}".format(error))
            raise

    def get_resource_records(self, **kwargs):
        """Get record list for a specified DNS zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: Record list
        :rtype: list
        """
        # Required parameters
        args = ['dns_zone', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
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
            print("Error getting resource records. {}".format(error))
            raise

    def delete_resource_record(self, **kwargs):
        """Delete record in a specified zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param record: Record name to delete
        :type record: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        """
        # Required parameters
        args = ['dns_zone', 'record', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        # Get zone ID and resource instane GUID
        zone_id = self.get_dns_zone_id(
            dns_zone=args["dns_zone"],
            resource_instance=args["resource_instance"])

        # Get record ID
        record = self.get_resource_record(dns_zone=args["dns_zone"],
                                          resource_instance=args[
                                          "resource_instance"],
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
                return resource_deleted()
            return result

        except Exception as error:
            print("Error deleting zone. {}".format(error))
            raise
        else:
            return ({"errors": [{"code": "not_found",
                                 "message": "No dns record found"}]})

    def get_resource_record(self, **kwargs):
        """Get specific resource record from a DNS zone

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param record: Record name
        :type record: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: Record information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'record', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record': kwargs.get('record'),
        }

        # get resource instance guid
        temp_ri = self.resource_instance.get_resource_instance(
            args['resource_instance'])
        if "errors" in temp_ri:
            return temp_ri
        resource_instance_guid = temp_ri["guid"]

        by_name = self.get_resource_record_by_name(dns_zone=args[
                                'dns_zone'],
                                resource_instance=resource_instance_guid,
                                record_name=args['record'])
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_resource_record_by_id(dns_zone=args[
                                'dns_zone'],
                                resource_instance=resource_instance_guid,
                                record_id=args['record'])
                    if "errors" in by_id:
                        return by_id
                    return by_id
                return by_name
        else:
            return by_name

    def get_resource_record_by_name(self, **kwargs):
        """Get record by name

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param record_name: Record name
        :type record_name: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: Record information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'record_name', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record_name': kwargs.get('record_name'),
        }

        # Get list of records
        records = self.get_resource_records(
            dns_zone=args['dns_zone'],
            resource_instance=args["resource_instance"])['resource_records']
        for record in records:
            if record['name'] == args['record_name']:
                return record
        return ({"errors": [{"code": "not_found",
                "message": "No record found"}]})

    def get_resource_record_by_id(self, **kwargs):
        """Get record by ID

        :param dns_zone: DNS zone name
        :type dns_zone: str
        :param record_id: Record ID
        :type record_name: str
        :param resource_instance: Name or GUID of the resource instance
        :type resource_instance: str
        :return: Record information
        :rtype: dict
        """
        # Required parameters
        args = ['dns_zone', 'record_id', 'resource_instance']
        check_args(args, **kwargs)

        # Set default value if required paramaters are not defined
        args = {
            'dns_zone': kwargs.get('dns_zone'),
            'resource_instance': kwargs.get('resource_instance'),
            'record_id': kwargs.get('record_id'),
        }

        # Get zone ID and resource instane GUID
        records = self.get_resource_records(
            dns_zone=args['dns_zone'],
            resource_instance=args["resource_instance"])['resource_records']

        for record in records:
            if record['id'] == args['record_id']:
                return record
        return ({"errors": [{"code": "not_found",
                "message": "No record found"}]})
