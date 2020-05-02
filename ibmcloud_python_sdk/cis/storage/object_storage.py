# Copyright: (c) 2020, IBM Corp.

import json
import ibm_boto3

from botocore.client import Config

from ibmcloud_python_sdk.resource import resource_instance
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import resource_error
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

    def get_bucket(self, **kwargs): 
        """Return a bucket for the specified location and service 
           instance and bucket name.
        
        :param: bucket: bucket name
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with this
            bucket
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance')
        }
        # get all buckets
        buckets = self.get_buckets(mode=args["mode"],
                                   location=args["location"],
                                   service_instance=args["service_instance"])
        if 'errors' in buckets:
            return buckets
        
        for bucket in buckets:
            if bucket["Name"] == args["bucket"]:
                return bucket
        return resource_not_found()

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

    def create_bucket(self, **kwargs):
        """Return a list of buckets for the specified location and service 
           instance
        
        :param: acl:  private'|'public-read'|'public-read-write'
            |'authenticated-read' : default is private
        :param: bucket: bucket name
        :param: 
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance')
        }
        opt_args = {
            'Bucket': args["bucket"],
            'ACL': kwargs.get('acl') or 'private',
            'GrantFullControl': kwargs.get('grantfullcontrol'),
            'GrantRead': kwargs.get('grantread'),
            'GrantReadACP': kwargs.get('grantreadacp'),
            'GrantWrite': kwargs.get('grantwrite'),
            'GrantWriteACP': kwargs.get('grantwriteacp'),
            'IBMSSEKPEncryptionAlgorithm': kwargs.get('ibmssekpencryptionsalgorithm'),
            'IBMSSEKPCustomerRootKeyCrn': kwargs.get('ibmssekpcustomerrootkeycrn')
        }
        
        bucket_kwargs = {key: value for (key, value) in opt_args.items() 
                            if value is not (None and '')} 

        cos_client = self.create_cos_client(mode=args["mode"],
                            location=args["location"],
                            service_instance=args["service_instance"])
        try:
            cos_client.create_bucket(**bucket_kwargs)
        except Exception as error:
            return resource_error("unknown", error)
               
    def delete_bucket(self, **kwargs):
        """Delete the specified bucket
        
        :param: bucket: bucket name
        :param: location: buckets geo location
        :param: service_instance: service instance associated with the
            bucket
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance')
        }
        cos_client = self.create_cos_client(mode=args["mode"],
                            location=args["location"],
                            service_instance=args["service_instance"])
        
        page = cos_client.get_paginator('list_objects')

        try:
            # delete all objects in the buckets
            for page in page.paginate(Bucket=args["bucket"]):
                keys = [{'Key': obj['Key']} for obj in page.get('Contents', [])]
                if keys:
                    cos_client.delete_objects(Bucket=args["bucket"], 
                                Delete={'Objects': keys})
            # delete the bucket
            result = cos_client.delete_bucket(Bucket=args["bucket"])
            if result is None:
                return resource_deleted()
            else:
                return result
        except Exception as error:
            return resource_error("unknown", error)        

    def put_object(self, **kwargs):
        """Put an object in the bucket for the specified location and service 
           instance
        
        :param: acl: private'|'public-read'|'public-read-write'|
            'authenticated-read'|'aws-exec-read'|'bucket-owner-read'|
            'bucket-owner-full-control' : default is private.
        :param: bucket: bucket name
        :param: body: b'bytes'|file put in the bucket, 
        :param: key: object key for which the PUT operation was initiated : 
            object name.
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance'),
            'body': kwargs.get('body'),
            'key': kwargs.get('key'),
        }

        acl = kwargs.get('acl') or 'private'

        cos_client = self.create_cos_client(mode=args["mode"],
                    location=args["location"],
                    service_instance=args["service_instance"])
        
        try:
            cos_client.put_object(Bucket=args["bucket"],
                                  ACL=acl, 
                                  Body=args["body"],
                                  Key=args["key"])
        except Exception as error:
            return resource_error("unknown", error)      

    def get_object(self, **kwargs):
        """Put an object in the bucket for the specified location and service 
           instance

        :param: bucket: bucket name
        :param: key: object key for which the PUT operation was initiated : 
            object name.
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance'),
            'key': kwargs.get('key'),
        }

        cos_client = self.create_cos_client(mode=args["mode"],
                    location=args["location"],
                    service_instance=args["service_instance"])
        
        try:
            return cos_client.get_object(Bucket=args["bucket"],
                                  Key=args["key"])
        except Exception as error:
            return resource_error("unknown", error)      

    def get_objects(self, **kwargs):
        """Return a list of objects present in the bucket for the specified 
            location and service instance.

        :param: bucket: bucket name
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """

        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance'),
        }

        cos_client = self.create_cos_client(mode=args["mode"],
                    location=args["location"],
                    service_instance=args["service_instance"])
       
        page = cos_client.get_paginator('list_objects')
        objects = []
        try:
            for page in page.paginate(Bucket=args["bucket"]):
                objects.append(page.get('Contents', []))
            return objects
        except Exception as error:
            return resource_error("unknown", error)  


    def delete_object(self, **kwargs):
        """Delete an object in the bucket for the specified location and service 
           instance
    
        :param: bucket: bucket name
        :param: key: object key for which the PUT operation was initiated : 
            object name.
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance'),
            'key': kwargs.get('key'),
        }

        cos_client = self.create_cos_client(mode=args["mode"],
                    location=args["location"],
                    service_instance=args["service_instance"])
        
        try:
            result = cos_client.delete_object(Bucket=args["bucket"],
                                  Key=args["key"])
            if result is None:
                return resource_deleted()
            else:
                return(result)                
        except Exception as error:
            return resource_error("unknown", error)      


    def delete_objects(self, **kwargs):
        """Delete objects in the bucket for the specified location and service 
           instance
    
        :param: bucket: bucket name
        : 
        :param: mode: bucket mode(region, cross-region, etc...)
        :param: objects: list of object names to delete.
        :param: location: buckets geo location
        :param: service_instance: service instance associated with these 
            buckets
        """
        args = {
            'mode': kwargs.get('mode'),
            'bucket': kwargs.get('bucket'),
            'location': kwargs.get('location'),
            'service_instance': kwargs.get('service_instance'),
            'key': kwargs.get('key'),
            'objects': kwargs.get('objects'),
        }

        cos_client = self.create_cos_client(mode=args["mode"],
                    location=args["location"],
                    service_instance=args["service_instance"])      
        try:
            for obj in args["objects"]:
                result = cos_client.delete_object(Bucket=args["bucket"],
                                  Key=obj)
                if result["ResponseMetadata"]["HTTPStatusCode"] is not 204:
                    return(result)
            return resource_deleted()
        except Exception as error:
            return resource_error("unknown", error)      
