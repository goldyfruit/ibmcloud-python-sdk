from ibmcloud_python_sdk.utils import softlayer as sl
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_error
from ibmcloud_python_sdk.utils.common import check_args


class Order():

    def __init__(self):
        self.client = sl.client()
        self.order = sl.SoftLayer.OrderingManager(self.client)

    def get_operating_systems(self, package=None):
        """Retrieve baremetal operating systems

        :param package:  Optional. Package name.
        :return: Baremetal operating systems
        :rtype: dict
        """
        # Provided package should have "os" category code.
        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        filter = {"items": {"categories": {"categoryCode": {
            "operation": "_= os"}}}}
        mask = ("mask[id, keyName, description, itemCategory, categories,"
                "prices]")

        try:
            # Retrieve package ID base on package keyname
            pkg_id = self.order.get_package_by_key(pkg_name, mask='id')['id']

            images = {}
            images["operating_systems"] = self.client.call(
                "Product_Package", "getItems", id=pkg_id, filter=filter,
                mask=mask, iter=True)

            return images

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_operating_system(self, image, package=None):
        """Retrieve specific baremetal operating systems

        :param image: Image name.
        :param package: Optional. Package name.
        :return: Baremetal operating system
        :rtype: dict
        """
        # Package should have "os" category code.
        # By default BARE_METAL_SERVER will be used.
        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        try:
            # Retrieve operating systems
            data = self.get_operating_systems(pkg_name)

            # Loop over operating systems until filter match
            for operating_system in data["operating_systems"]:
                if operating_system["keyName"] == image:
                    # Return data
                    return operating_system

            # Return error if no operating system is found
            return resource_not_found()

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_package_items(self, package=None, **kwargs):
        """Retrieve baremetal operating systems

        :param package: Optional. Package name.
        :param category: Filter by category.
        :param mask: Mask fields.
        :return: Baremetal operating systems
        :rtype: dict
        """
        # Build dict of argument and assign default value when needed
        args = {
            'category': kwargs.get('category'),
            'mask': kwargs.get('mask'),
        }

        filter = None
        if args['category']:
            filter = {"items": {"categories": {"categoryCode": {
                "operation": "_= {}".format(args['category'])}}}}

        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        mask = "id, keyName, description"

        try:
            packages = {}
            packages["items"] = self.order.list_items(pkg_name, mask=mask,
                                                      filter=filter)

            return packages

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_package_presets(self, package=None):
        """Retrieve baremetal package presets

        :param package: Optional. Package name.
        :return: Baremetal presets from package
        :rtype: dict
        """
        pkg_name = "BARE_METAL_SERVER"
        if package:
            pkg_name = package

        try:
            packages = {}
            packages["presets"] = self.order.list_presets(pkg_name)

            return packages

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def get_locations(self):
        """Retrieve all datacenter locations

        :return: List of datacenter location
        :rtype: dict
        """
        mask = "id,name,regions[keyname,description]"
        try:
            locations = {}
            locations["datacenters"] = self.client.call(
                "SoftLayer_Location", "getDatacenters", mask=mask)

            return locations

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def verify(self, **kwargs):
        """Verify an order

        :param package: The package being ordered.
        :param location: The datacenter location string for ordering.
        :param items: The list of item keyname strings to order.
        :param complex_type: The complex type to send with the order.
        :param hourly: Optional. If true, uses hourly billing.
        :param preset: Optional. Specifies a preset to use for that package.
        :param extras: The extra data for the order in dictionary format.
        :param quantity: Optional. The number of resources to order.
        :return: The verified order
        :rtype: dict
        """
        args = ["package", "location", "items", "complex_type", "extras"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'package': kwargs.get('package'),
            'location': kwargs.get('location'),
            'items': kwargs.get('items'),
            'complex_type': kwargs.get('complex_type'),
            'hourly': kwargs.get('hourly', True),
            'preset': kwargs.get('preset'),
            'extras': kwargs.get('extras'),
            'quantity': kwargs.get('quantity', 1),
        }

        try:
            return self.order.verify_order(
                args['package'], args['location'], args['items'],
                hourly=args['hourly'], preset_keyname=args['preset'],
                complex_type=args['complex_type'], extras=args['extras'],
                quantity=args['quantity'])

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)

    def place(self, **kwargs):
        """Place an order

        :param package: The package being ordered.
        :param location: The datacenter location string for ordering.
        :param items: The list of item keyname strings to order.
        :param complex_type: The complex type to send with the order.
        :param hourly: Optional. If true, uses hourly billing.
        :param preset: Optional. Specifies a preset to use for that package.
        :param extras: The extra data for the order in dictionary format.
        :param quantity: Optional. The number of resources to order.
        :return: The placed order
        :rtype: dict
        """
        args = ["package", "location", "items", "complex_type", "extras"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'package': kwargs.get('package'),
            'location': kwargs.get('location'),
            'items': kwargs.get('items'),
            'complex_type': kwargs.get('complex_type'),
            'hourly': kwargs.get('hourly', True),
            'preset': kwargs.get('preset'),
            'extras': kwargs.get('extras'),
            'quantity': kwargs.get('quantity', 1),
        }

        try:
            return self.order.place_order(
                args['package'], args['location'], args['items'],
                hourly=args['hourly'], preset_keyname=args['preset'],
                complex_type=args['complex_type'], extras=args['extras'],
                quantity=args['quantity'])

        except sl.SoftLayer.SoftLayerAPIError as error:
            return resource_error(error.faultCode, error.faultString)
