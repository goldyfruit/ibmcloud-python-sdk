import json
import SoftLayer

from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found

from ibmcloud_python_sdk.utils.common import check_args

from SoftLayer import DNSManager

class Dns():

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
            return (self.dns.create_zone(zone, serial))
        except Exception as error:
            print(f"Error creating dns zones. {error}")
            raise
       


    # List all domains
    def list_zones(self, **kwargs):
        try:
            return (self.dns.list_zones(**kwargs))
        except Exception as error:
            print(f"Error listing dns zones. {error}")
            raise


    def create_record(self, **kwargs):
        """Create a resource record on a domain.

        :param integer id: the zone's ID
        :param record: the name of the record to add
        :param record_type: the type of record (A, AAAA, CNAME, TXT, etc.)
        :param data: the record's value
        :param integer ttl: the TTL or time-to-live value (default: 60)
        """
        required_args = set(["zone", "record", "record_type",
            "data", "ttl"])
        check_args(required_args, **kwargs)

        # Set default value is not required paramaters are not defined
        args = {
            'zone': kwargs.get('zone'),
            'record': kwargs.get('record'),
            'record_type': kwargs.get('record_type'),
            'data': kwargs.get('data'),
            'ttl': kwargs.get('ttl') or '60',
        }
        try:
            return (self.dns.create_record(args['zone'], args['record'], 
                args['record_type'], args['data'], args['ttl']))
        except Exception as error:
            print(f"Error creating dns record. {error}")
            raise

    def delete_recore(self, **kwargs):
        pass
