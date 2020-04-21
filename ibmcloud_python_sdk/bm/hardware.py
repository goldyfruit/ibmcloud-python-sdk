from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_not_found


class Hardware():

    def __init__(self):
        self.client = sl.client()
        self.hw = sl.SoftLayer.HardwareManager(self.client)

    def get_baremetals(self):
        """
        Retrieve baremetal list
        :return List of baremetal servers
        """
        try:
            return self.hw.list_hardware()
        except sl.SoftLayer.SoftLayerAPIError as error:
            print("Error fetching baremetals. {}".format(error))
            raise

    def get_baremetal(self, baremetal):
        """
        Retrieve specific baremetal
        :param baremetal: Baremetal name or ID
        :return Baremetal server information as a dict
        """
        by_name = self.get_baremetal_by_name(baremetal)
        if "errors" in by_name:
            by_id = self.get_baremetal_by_id(baremetal)
            if "errors" in by_id:
                return by_id
            else:
                return by_id
        else:
            return by_name

    def get_baremetal_by_id(self, id):
        """
        Retrieve specific baremetal by ID
        :param id: baremetal ID
        :return Baremetal server information as a dict
        """
        try:
            return self.hw.get_hardware(id)
        except sl.SoftLayer.SoftLayerAPIError as error:
            print("Error fetching baremetal with ID {}. {}".format(id, error))
            raise

    def get_baremetal_by_name(self, name):
        """
        Retrieve specific baremetal by name
        :param name: Baremetal name
        :return Baremetal server information as a dict
        """
        try:
            # Retrieve baremetals
            data = self.get_baremetals()

            # Loop over baremetals until filter match
            for baremetal in data:
                if baremetal["fullyQualifiedDomainName"] == name:
                    # Return data
                    return self.hw.get_hardware(baremetal["id"])

            # Return error if no baremetal is found
            return resource_not_found()

        except sl.SoftLayer.SoftLayerAPIError as error:
            print("Error fetching baremetal with name {}. {}".format(
                name, error))
            raise
