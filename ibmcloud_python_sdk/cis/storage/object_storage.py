# Copyright: (c) 2020, IBM Corp.

import json
import ibm_boto3

from botocore.client import Config

from ibmcloud_python_sdk import resource_instance
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.utils.object_regions import endpoints

class ObjectStorage():

    def __init__(self):
        self.cfg = params()
        self.ri = resource_instance.ResourceInstance()
        
    def get_endpoint(self, **kwargs):
        """Get endppoint storage url from lookup based on mode and location

        :param: mode: access mode .. default value is regional
        :param: location: region tom host the bucket. default value is us-south
        """

        args = {
            'mode': kwargs.get('mode') or 'regional',
            'location':  kwargs.get('location') or 'us-south',
        }
        try:
            return ("https://{}".format(
                endpoints[args["mode"]][args["location"]]))

        except Exception:
            return resource_not_found()

    def create_cos_client(self, **kwargs):
        """Create object to manage buckets
        """
        
        args = {
            'mode': kwargs.get('mode'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance')
        }
        
        service_endpoint = self.get_endpoint(mode=args["mode"], 
                                        location=args["location"])
        
        if "errors" in service_endpoint:
            for key_name in service_endpoint["errors"]:
                if key_name["code"] == "not_found":
                    return resource_not_found()

        service_instance = self.ri.get_resource_instance(
                    args["service_instance"])

        if "errors" in service_instance:
            for key_name in service_instance["errors"]:
                if key_name["code"] == "not_found":
                    return resource_not_found()        

        cos_client = ibm_boto3.client('s3', 
                        ibm_api_key_id = self.cfg["key"], 
                        ibm_service_instance_id=service_instance["id"], 
                        config=Config(signature_version='oauth'), 
                        endpoint_url=service_endpoint)
        return cos_client

    
    def get_buckets(self, **kwargs):
        """Return a list of buckets for the specified location and service 
           instance
        
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance')
        }

        cos_client = self.create_cos_client(mode=args["mode"],
                            location=args["location"],
                            service_instance=args["service_instance"])

        if isinstance(cos_client, dict):
            if "errors" in cos_client:
                return resource_not_found()
        return cos_client.list_buckets()['Buckets']
                    
    # def get_network_acls(self):
    #     """