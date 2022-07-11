from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_error


class Vlan():

    def __init__(self):
        self.client = sl.client()
        self.nm = sl.SoftLayer.NetworkManager(self.client)

    def get_vlans(self):
        """Retrieve vlan list

        :return: List of vlans
        :rtype: dict
        """
        try:
            vlan = {}
            vlan["vlans"] = self.nm.list_vlans()

            return vlan

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)
