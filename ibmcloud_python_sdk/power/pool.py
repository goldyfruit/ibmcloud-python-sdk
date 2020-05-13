from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers


class Pool():

    def __init__(self):
        self.cfg = params()

    def get_pools(self, instance):
        """Retrieve system pools for a specific cloud instance

        :param instance: Cloud instance ID
        :return List of system pools
        :rtype dict
        """
        try:
            # Connect to api endpoint for system-pools
            path = ("/pcloud/v1/cloud-instances/{}/system-pools".format(
                instance))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching system pools for cloud instance {}."
                  " {}".format(instance, error))
