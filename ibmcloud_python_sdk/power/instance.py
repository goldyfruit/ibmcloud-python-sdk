from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_deleted


class Instance():

    def __init__(self):
        self.cfg = params()

    def get_instance(self, instance):
        """Retrieve information about cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: Cloud instance information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}".format(instance))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching cloud instance {}. {}".format(
                instance, error))

    def delete_instance(self, instance):
        """Delete cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for sshkeys
            path = ("/pcloud/v1/cloud-instances/{}".format(ci_info["name"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting cloud instance {}. {}".format(
                instance, error))
