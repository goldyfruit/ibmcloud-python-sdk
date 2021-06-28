from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import resource_created
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.cis.storage import client


class Bucket():

    def __init__(self, **kwargs):
        self.cfg = params()
        self.client = client.cos_client(
            mode=kwargs.get('mode', 'regional'),
            location=kwargs.get('location', self.cfg['region']),
            service_instance=kwargs.get('service_instance')
        )

    def get_buckets(self):
        """Retrieve bucket list

        :return List of buckets
        :rtype dict
        """
        try:
            data = self.client.list_buckets()

            return data['Buckets']

        except Exception as error:
            return resource_error("unable_to_fetch_bucket_list", error)

    def get_bucket(self, bucket):
        """Retrieve specific bucket

        :param bucket: Bucket name
        :type bucket: str
        :return: Bucket information
        :rtype: dict
        """
        try:
            # Retrieve buckets
            data = self.get_buckets()
            if "errors" in data:
                return data

            # Loop over buckets until filter match
            for bucket_info in data:
                if bucket_info["Name"] == bucket:
                    # Return data
                    return bucket_info

            # Return error if no bucket is found
            return resource_not_found()

        except Exception as error:
            return resource_error("unable_to_fetch_bucket", error)

    def create_bucket(self, **kwargs):
        """Create bucket

        :param bucket: Bucket name
        :type bucket: str
        :param acl: The canned ACL to apply to the bucket
        :type acl: str
        :param grant_full_control: Allows grantee the read, write, read ACP,
            and write ACP permissions on the bucket
        :type grant_full_control: str
        :param grant_read: Allows grantee to list the objects in the bucket
        :type grant_read: str
        :param grant_read_acp: Allows grantee to read the bucket ACL
        :type grant_read_acp: str
        :param grant_write: Allows grantee to create, overwrite, and delete
            any object in the bucket
        :type grant_write: str
        :param grant_write_acp: Allows grantee to write the ACL for the
            applicable bucket
        :type grant_write_acp: str
        :param ibm_sse_kp_encryptions_algorithm: The encryption algorithm that
            will be used for objects stored in the newly created bucket
        :type ibm_sse_kp_encryptions_algorithm: str
        :param ibm_sse_kp_customer_root_key_crn: Container for describing the
            KMS-KP Key CRN
        :type ibm_sse_kp_customer_root_key_crn: str
        :return: Bucket creation status
        :rtype: dict
        """
        args = ["bucket"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'Bucket': kwargs.get('bucket'),
            'ACL': kwargs.get('acl', 'private'),
            'GrantFullControl': kwargs.get('grant_full_control'),
            'GrantRead': kwargs.get('grant_read'),
            'GrantReadACP': kwargs.get('grant_read_acp'),
            'GrantWrite': kwargs.get('grant_write'),
            'GrantWriteACP': kwargs.get('grant_write_acp'),
            'IBMSSEKPEncryptionAlgorithm': kwargs.get(
                'ibm_sse_kp_encryptions_algorithm'),
            'IBMSSEKPCustomerRootKeyCrn': kwargs.get(
                'ibm_sse_kp_customer_root_key_crn')
        }

        payload = {
            key: value for (key, value) in args.items() if value is not None}

        try:
            result = self.client.create_bucket(**payload)
            if result["ResponseMetadata"]["HTTPStatusCode"] != 200:
                return result

            msg = {"bucket": args['Bucket'], "status": "created"}
            return resource_created(msg)

        except Exception as error:
            return resource_error("unable_to_create", error)

    def delete_bucket(self, bucket):
        """Delete bucket

        :param bucket: Bucket name
        :type bucklet: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            # Pagination
            p = self.client.get_paginator('list_objects')

            # Delete objects (1000 objects max at a time)
            for page in p.paginate(Bucket=bucket):
                keys = [
                    {'Key': obj['Key']} for obj in page.get('Contents', [])
                ]
                if keys:
                    self.client.delete_objects(Bucket=bucket,
                                               Delete={'Objects': keys})

            result = self.client.delete_bucket(Bucket=bucket)
            if result["ResponseMetadata"]["HTTPStatusCode"] != 204:
                return result

            return resource_deleted()

        except Exception as error:
            return resource_error("unable_to_delete", error)
