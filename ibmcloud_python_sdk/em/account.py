from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Account():

    def __init__(self):
        self.cfg = params()

    def get_accounts(self):
        """Retrieve account list

        :return: List of accounts
        :rtype: list
        """
        try:
            # Connect to api endpoint for accounts
            path = ("/v1/accounts")

            # Return data
            return qw("em", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching accounts. {}".format(error))
            raise
