from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import resource_created
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.cis.storage import client
from ibmcloud_python_sdk.cis.storage import bucket


class Object():

    def __init__(self, **kwargs):
        self.cfg = params()
        self.client = client.cos_client(
            mode=kwargs.get('mode', 'regional'),
            location=kwargs.get('location', self.cfg['region']),
            service_instance=kwargs.get('service_instance')
        )
        self.bucket = bucket.Bucket(
            mode=kwargs.get('mode', 'regional'),
            location=kwargs.get('location', self.cfg['region']),
            service_instance=kwargs.get('service_instance')
            )

    def get_objects(self, bucket):
        """Retrieve objects list from a bucket

        :param bucket: Bucket name
        :type bucket: str
        :return: List of objects
        :rtype: dict
        """
        try:
            p = self.client.get_paginator('list_objects')
            objects = []

            for page in p.paginate(Bucket=bucket):
                objects.append(page.get('Contents', []))
            return objects

        except Exception as error:
            print("Error fetching object list from bucket {}. {}".format(
                bucket, error))

    def get_object(self, bucket, object):
        """Retrieve specific object form a bucket

        :param bucket: Bucket name
        :type bucket: str
        :param object: Object name
        :type object: str
        :return: Object information
        :rtype: dict
        """
        try:
            # Check if bucket exists and retrieve information
            bucket_info = self.bucket.get_bucket(bucket)
            if "errors" in bucket_info:
                return bucket_info

            return self.client.get_object(Bucket=bucket_info["Name"],
                                          Key=object)

        except Exception as error:
            payload = {"errors": [{"message": error}]}
            return resource_not_found(payload)

    def put_object(self, **kwargs):
        """Adds an object to a bucket

        :param acl: The canned ACL to apply to the object
        :type acl: str
        :param bucket: Bucket name
        :type bucket: str
        :param body: Object data
        :type body: str
        :param key: Object key for which the PUT operation was initiated
        :type key: str
        :return: Upload status
        :rtype: dict
        """
        args = ["bucket", "body", "key"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'acl': kwargs.get('acl', 'private'),
            'bucket': kwargs.get('bucket'),
            'body': kwargs.get('body'),
            'key': kwargs.get('key'),
        }

        try:
            result = self.client.put_object(
                Bucket=args["bucket"],
                ACL=args['acl'],
                Body=args["body"],
                Key=args["key"]
            )
            if result["ResponseMetadata"]["HTTPStatusCode"] != 200:
                return result

            msg = {"object": args["key"], "bucket": args['bucket'],
                   "status": "created"}
            return resource_created(msg)

        except Exception as error:
            return resource_error("unable_to_put_object", error)

    def upload_file(self, **kwargs):
        """Upload a file to an S3 object

        :param bucket: Bucket name
        :type bucket: str
        :param path: The path to the file to upload
        :type path: str
        :param key: The name of the key to upload to
        :type key: str
        :return: Upload status
        :rtype: dict
        """
        args = ["bucket", "path", "key"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'bucket': kwargs.get('bucket'),
            'key': kwargs.get('key'),
            'path': kwargs.get('path'),
        }

        try:
            result = self.client.upload_file(
                args["path"], args["bucket"], args["key"])
            if result is not None:
                return result

            msg = {"object": args["key"], "bucket": args['bucket'],
                   "status": "created"}
            return resource_created(msg)

        except Exception as error:
            return resource_error("unable_to_upload_object", error)

    def download_file(self, **kwargs):
        """Download file from a S3 object

        :param bucket: Bucket name
        :type bucket: str
        :param path: The path to the file to download to
        :type path: str
        :param key: The name of the key to download from
        :type key: str
        :return: Download status
        :rtype: dict
        """
        args = ["bucket", "path", "key"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'bucket': kwargs.get('bucket'),
            'key': kwargs.get('key'),
            'path': kwargs.get('path'),
        }

        try:
            result = self.client.download_file(
                args["bucket"], args["key"], args["path"])
            if result is not None:
                return result

            msg = {"object": args["key"], "path": args['path'],
                   "status": "downloaded"}
            return resource_created(msg)

        except Exception as error:
            return resource_error("unable_to_download_object", error)

    def delete_object(self, bucket, object):
        """Delete an object from the bucket

        :param bucket: Bucket name
        :type bucket: str
        :param object: The name of the object to delete
        :type object: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            result = self.client.delete_object(Bucket=bucket, Key=object)
            if result["ResponseMetadata"]["HTTPStatusCode"] != 204:
                return result

            return resource_deleted()

        except Exception as error:
            return resource_error("unable_to_delete_object", error)

    def delete_objects(self, bucket, objects):
        """Delete objects from the bucket

        :param bucket: Bucket name
        :type bucket: str
        :param objects: List of objects to delete
        :type objects: list
        """
        try:
            for object in objects:
                result = self.client.delete_object(Bucket=bucket, Key=object)
                if result["ResponseMetadata"]["HTTPStatusCode"] != 204:
                    return result

            return resource_deleted()

        except Exception as error:
            return resource_error("unable_to_delete_objects", error)
