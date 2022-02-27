from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_error


class Subnet():

    DEFAULT_SUBNET_MASK = ','.join(['hardware',
                                    'ipAddresses',
                                    'datacenter',
                                    'networkVlanId',
                                    'ipAddressCount',
                                    'virtualGuests',
                                    'id',
                                    'networkIdentifier',
                                    'cidr',
                                    'subnetType',
                                    'gateway',
                                    'broadcastAddress',
                                    'usableIpAddressCount',
                                    'note',
                                    'tagReferences[tag]',
                                    'networkVlan[id,networkSpace]'])
    def __init__(self):
        self.client = sl.client()
        self.hw = sl.SoftLayer.NetworkManager(self.client)

    def get_subnets(self):
        """Retrieve subnet list

        :return: List of subnet servers
        :rtype: dict
        """
        # Display all the fields.
        mask = ""
        try:
            subnets = {}
            subnets = self.hw.list_subnets(mask=self.DEFAULT_SUBNET_MASK)

            return subnets

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_subnet_by_id(self, id):
        """Retrieve specific subnet by ID

        :param id: Subnet ID
        :type id: str
        :return: Subnet server information
        :rtype: dict
        """
        try:
            return self.hw.get_subnet(id, mask=self.DEFAULT_SUBNET_MASK)

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)
