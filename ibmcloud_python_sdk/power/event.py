from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.power import instance


class Event():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_events(self, instance, time):
        """Retrieve event list from a timestamp for a specific cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param time: A time in either ISO 8601 or unix epoch format
        :type time: str
        :return: List of events
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/events?time={}".format(
                ci_info["name"], time))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching events for cloud instance {}. {}".format(
                instance, error))

    def get_event(self, instance, event):
        """Retrieve specific event for a specific cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param event: Event ID
        :type event: str
        :return: Event information
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/events/{}".format(
                ci_info["name"], event))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching event {} for cloud instance {}. {}".format(
                event, instance, error))
