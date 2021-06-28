import ibm_boto3
import re

from ibmcloud_python_sdk.utils.object_regions import endpoints
from ibmcloud_python_sdk.resource import resource_instance
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import decode_token
from botocore.client import Config


def _get_endpoint(**kwargs):
    """Get endpoint storage URL from lookup based on mode and region

    :param mode: Access mode
    :type mode: str
    :param region: Region where to host the bucket
    :type region: str
    :return URL endpoint
    :rtype: str
    """
    args = {
        'mode': kwargs.get('mode', 'regional'),
        'region': kwargs.get('region', 'us-south'),
    }

    try:
        url = "https://{}".format(endpoints[args["mode"]][args["region"]])
        return url

    except Exception:
        return resource_not_found()


def cos_client(**kwargs):
    """Create Cloud Object Storage client

    :param mode: Access mode
    :type mode: str
    :param location: Region where to host the bucket
    :type location: str
    :param service_instance: Resource instance name or ID
    :type service_instance: str
    :return: Cloud Object Storage client
    :rtype: dict
    """
    cfg = params()

    # Build dict of argument and assign default value when needed
    args = {
        'mode': kwargs.get('mode'),
        'location': kwargs.get('location'),
        'service_instance': kwargs.get('service_instance'),
        'account': kwargs.get('account', decode_token()['account']['bss']),
    }
    ri = resource_instance.ResourceInstance()

    try:
        # Check if endpoint exists
        endpoint = _get_endpoint(mode=args["mode"], location=args["location"])
        if "errors" in endpoint:
            return endpoint

        ri_info = None
        if args['service_instance']:
            # Check if resource instance exists and retrieve information
            ri_info = ri.get_resource_instance(args["service_instance"])
            if "errors" in ri_info:
                return ri_info
        else:
            # Automatically detect if cloud-object-storage service exists.
            # If multiple resource instance exist then the last one to match
            # the regex will be used.
            service = "cloud-object-storage"
            regex = "crn:v1:bluemix:public:{}:global:a/{}".format(
                service, args['account'])
            data = ri.get_resource_instances()
            for instance in data['resources']:
                if re.search(regex, instance['id']):
                    ri_info = instance

        client = ibm_boto3.client(
            's3',
            ibm_api_key_id=cfg["key"],
            ibm_service_instance_id=ri_info['id'],
            config=Config(signature_version='oauth'),
            endpoint_url=endpoint
        )

        return client

    except Exception as error:
        print("Error creating Cloud Object Storage client. {}".format(error))
