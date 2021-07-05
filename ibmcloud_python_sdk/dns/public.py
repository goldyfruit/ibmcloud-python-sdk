import SoftLayer

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import check_args


class Dns():
    """Public dns class
    """

    def __init__(self):
        self.cfg = params()
        self.client = SoftLayer.create_client_from_env(
            username=self.cfg['cis_username'],
            api_key=self.cfg['cis_apikey'])
        self.dns = SoftLayer.DNSManager(self.client)

    def create_zone(self, zone, serial=None):
        """Create a zone for the specified zone

        :param zone: Zone name
        :type zone: str
        :param serial: serial value on the zone, defaults to
            `strftime(%Y%m%d01)`
        :type serial: str
        """
        try:
            return self.dns.create_zone(zone, serial)
        except Exception as error:
            print("Error creating dns zones. {}".format(error))
            raise

    def create_record(self, **kwargs):
        """Create a resource record on a domain

        :param zone: Zone name
        :type zone: str
        :param record: Record name
        :type record: str
        :param record_type: Type of record (A, AAAA, CNAME, TXT, etc...)
        :type record_type: str
        :param data: Record's value
        :type data: str
        :param ttl: Time-To-Live, defaults to `60`
        :type ttl: int
        """
        args = set(["zone", "record", "record_type", "data"])
        check_args(args, **kwargs)

        zone_id = self.get_zone_id(kwargs.get('zone'))
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key_name in zone_id["errors"]:
                    if key_name["code"] == "not_found":
                        return resource_not_found()
                    return zone_id
        # Set default value is not required paramaters are not defined
        args = {
            'zone': zone_id,
            'record': kwargs.get('record'),
            'record_type': kwargs.get('record_type'),
            'data': kwargs.get('data'),
            'ttl': kwargs.get('ttl', 60),
        }
        try:
            return (self.dns.create_record(args['zone'], args['record'],
                                           args['record_type'],
                                           args['data'], args['ttl']))
        except Exception as error:
            print("Error creating dns record. {}".format(error))
            raise

    def get_records(self, **kwargs):
        """Get record list for a specified zone

        :param zone: Zone name
        :type zone: str
        """
        zone_id = self.get_zone_id(kwargs.get('zone'))
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key_name in zone_id["errors"]:
                    if key_name["code"] == "not_found":
                        return resource_not_found()
                    return zone_id
        # Build dict of argument and assign default value when needed
        args = {
            'ttl': kwargs.get('ttl') or None,
            'data': kwargs.get('data') or None,
            'host': kwargs.get('host') or None,
            'record_type': kwargs.get('record_type') or None
        }
        return self.dns.get_records(zone_id=zone_id, **args)

    def get_zone_id(self, name):
        """Get zone id
        :param name: zone name
        """
        zones = self.list_zones()
        for zone in zones:
            if zone["name"] == name:
                return zone["id"]
        return resource_not_found()

    def list_zones(self, **kwargs):
        """Get all zones
        """
        try:
            return self.dns.list_zones(**kwargs)
        except Exception as error:
            print("Error listing dns zones. {}".format(error))
            raise

    def delete_zone(self, name):
        """Delete a zone
        """
        zone_id = self.get_zone_id(name)
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key_name in zone_id["errors"]:
                    if key_name["code"] == "not_found":
                        return zone_id
        try:
            self.dns.delete_zone(zone_id)
        except Exception as error:
            print("Error deleting dns zone. {}".format(error))
            raise

    def get_record(self, **kwargs):
        """Find a record by name or value
        """
        required_args = set(["record", "zone"])
        check_args(required_args, **kwargs)

        args = {
            'record': kwargs.get('record'),
            'zone': kwargs.get('zone'),
        }

        by_name = self.get_record_by_name(record=args["record"],
                                          zone=args["zone"])
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_value = self.get_record_by_value(record=args["record"],
                                                        zone=args["zone"])
                    if "errors" in by_value:
                        return by_value
                    return by_value
                return by_name
        return by_name

    def get_record_by_name(self, **kwargs):
        """Get record by name

        :param record: Record name
        :type record: str
        :param zone: Zone name
        :type zone: str
        """
        required_args = set(["record", "zone"])
        check_args(required_args, **kwargs)

        args = {
            'record': kwargs.get('record'),
            'zone': kwargs.get('zone'),
        }
        zone_id = self.get_zone_id(args['zone'])
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key_name in zone_id["errors"]:
                    if key_name["code"] == "not_found":
                        return resource_not_found()

        records = self.get_records(zone=args["zone"])
        for record in records:
            if record["host"] == args["record"]:
                return record
        return resource_not_found()

    def get_record_by_value(self, **kwargs):
        """Get record by value
        
        :param record: Record value
        :type record: str
        :param zone: Zone name
        :type zone: str
        """
        args = set(["record", "zone"])
        check_args(args, **kwargs)

        args = {
            'record': kwargs.get('record'),
            'zone': kwargs.get('zone'),
        }

        records = self.get_records(zone=args["zone"])
        if "errors" in records:
            for key_name in records["errors"]:
                if key_name["code"] == "not_found":
                    return resource_not_found()

        for record in records:
            if record["data"] == args["record"]:
                return record
        return resource_not_found()

    def delete_record(self, **kwargs):
        """Delete a record

        :param record: Record name
        :type record: str
        :param zone: Zone name
        :type zone: str
        """
        args = set(["record", "zone"])
        check_args(args, **kwargs)

        args = {
            'record': kwargs.get('record'),
            'zone': kwargs.get('zone'),
        }
        record = self.get_record(record=args["record"],
                                 zone=args["zone"])
        if "errors" in record:
            for key_name in record["errors"]:
                if key_name["code"] == "not_found":
                    return resource_not_found()
        try:
            self.dns.delete_record(record["id"])
        except Exception as error:
            print("Error while deleting record. {}".format(error))
            raise

    def check_availability(self, **kwargs):
        """Check zone availability
        """
        pass
