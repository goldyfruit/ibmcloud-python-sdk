import re
from ibmcloud_python_sdk.utils import constants
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import decode_token
from ibmcloud_python_sdk.resource import resource_instance
from ibmcloud_python_sdk.auth import get_token

cfg = params()
ri = resource_instance.ResourceInstance()
power_headers = {}


def get_power_headers(**kwargs):
    """Generates the headers used for Power authenticated HTTP request.

    This function is only used by the power package which is why it's in
    the __init__.py file. It replace the get_headers() method from auth.py.

    :param region: Region where the resource instance is created.
    :param account: Account ID.
    :parem instance: Resource instance name or ID.
    :return: Dict of headers
    :rtype: dict
    """
    # Build dict of argument and assign default value when needed
    args = {
        'region': kwargs.get('region', cfg["region"]),
        'account': kwargs.get('account', decode_token()['account']['bss']),
        'instance': kwargs.get('instance'),
    }

    ri_info = None
    if not power_headers:
        if args['instance']:
            ri_info = ri.get_resource_instance(args['instance'])
        else:
            # Automatically detect if power-iaas service exists.
            regex = "crn:v1:bluemix:public:power-iaas:{}:a/{}".format(
                args['region'], args['account'])
            data = ri.get_resource_instances()
            for instance in data['resources']:
                if re.search(regex, instance['id']):
                    ri_info = instance['id']

        # Return empty headers if resource instance doesn't exist which will
        # result to a 401.
        if not ri_info:
            return power_headers

        power_headers["Content-Type"] = "application/json"
        power_headers["Accept"] = "application/json"
        power_headers["User-Agent"] = constants.USER_AGENT
        power_headers["Authorization"] = get_token(
            constants.AUTH_URL, cfg["key"])
        power_headers['CRN'] = ri_info

        return power_headers

    return power_headers
