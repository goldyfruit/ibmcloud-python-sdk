import json
import SoftLayer

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import check_args

from SoftLayer import DNSManager

class Dns():
    """Dns public class
    """
    def __init__(self):
        self.cfg = params()
        self.client = SoftLayer.create_client_from_env(
            username=self.cfg['cis_username'],
            api_key=self.cfg['cis_apikey'])
        self.dns = DNSManager(self.client)


    # Create zone
    def create_zone(self, zone, serial=None):
        """Create a zone for the specified zone.

        :param zone: the zone name to create
        :param serial: serial value on the zone (default: strftime(%Y%m%d01))
         """
        try:
            return self.dns.create_zone(zone, serial)
        except Exception as error:
            print("Error creating dns zones. {}".format(error))
            raise

    # Create a record
    def create_record(self, **kwargs):
        """Create a resource record on a domain.

        :param integer id: the zone's ID
        :param record: the name of the record to add
        :param record_type: the type of record (A, AAAA, CNAME, TXT, etc.)
        :param data: the record's value
        :param integer ttl: the TTL or time-to-live value (default: 60)
        """
        required_args = set(["zone", "record", "record_type",
                             "data"])
        check_args(required_args, **kwargs)

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
            'ttl': kwargs.get('ttl') or '60',
        }
        try:
            return (self.dns.create_record(args['zone'], args['record'],
                                           args['record_type'],
                                           args['data'], args['ttl']))
        except Exception as error:
            print("Error creating dns record. {}".format(error))
            raise

    # Get records
    def get_records(self, **kwargs):
        """Get records for a specified name
        :param name: zone name
        """
        zone_id = self.get_zone_id(kwargs.get('name'))
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
            'host': kwargs.get('host')or None,
            'record_type': kwargs.get('record_type') or None
        }
        return self.dns.get_records(zone_id=zone_id, **args)


    # Get zone id
    def get_zone_id(self, name):
        """Get zone id
        :param name: zone name
        """
        zones = self.list_zones()
        for zone in zones:
            if zone["name"] == name:
                return zone["id"]
        return resource_not_found()


    # List all domains
    def list_zones(self, **kwargs):
        """Get all zones
        """
        try:
            return self.dns.list_zones(**kwargs)
        except Exception as error:
            print("Error listing dns zones. {}".format(error))
            raise


    # Delete a zone
    def delete_zone(self, name):
        """Delete a zone
        """
        zone_id = self.get_zone_id(name)
        return self.dns.delete_zone(zone_id)

    # Find a record by name
    def get_record_by_name(self, name):
        """Get record by name
        """
        pass


    def delete_record(self, **kwargs):
        """Delete a record
        """
        pass

    def check_availability(self, **kwargs):
        """Check zone availability
        """
        pass
