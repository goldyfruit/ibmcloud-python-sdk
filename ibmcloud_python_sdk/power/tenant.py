from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers


class Tenant():

    def __init__(self):
        self.cfg = params()

    def get_state(self, tenant):
        """Retrieve tenant state

        :param tenant: Tenant ID (Account ID)
        :type tenant: str
        :return: Tenant information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for tenants
            path = ("/pcloud/v1/tenants/{}".format(tenant))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching information for tenant {}. {}".format(
                tenant, error))
