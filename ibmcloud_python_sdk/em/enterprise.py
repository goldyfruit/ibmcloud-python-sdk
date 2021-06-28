from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Enterprise():

    def __init__(self):
        self.cfg = params()

    def get_enterprises(self):
        """Retrieve enterprise list

        :return: List of enterprises
        :rtype: list
        """
        try:
            # Connect to api endpoint for enterprises
            path = ("/v1/enterprises")

            # Return data
            return qw("em", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching enterprises. {}".format(error))
            raise
