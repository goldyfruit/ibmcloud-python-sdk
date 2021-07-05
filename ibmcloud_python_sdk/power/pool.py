from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.power import instance


class Pool():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_pools(self, instance):
        """Retrieve system pools for a specific cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: List of system pools
        :rtype: list
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for system-pools
            path = ("/pcloud/v1/cloud-instances/{}/system-pools".format(
                ci_info["name"]))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching system pools for cloud instance {}."
                  " {}".format(instance, error))
