from ibmcloud_python_sdk.resource import resource_group
import unittest


from mock import patch
from ibmcloud_python_sdk.vpc.subnet import Subnet

import tests.Common as Common

from tests.Subnet import Subnet as subnet


class FloatingIPTestCase(unittest.TestCase):
    """Test case for the client methods."""

    def setUp(self):
        self.patcher = patch('ibmcloud_python_sdk.auth.get_token',
                             subnet.authentication)
        self.patcher.start()
        self.subnet = Subnet()

    def tearDown(self):
        self.patcher.stop()

# get_subnets

# get_subnet
# get_subnet_by_id
# get_subnet_by_name
# get_subnet_network_acl
# get_subnet_public_gateway
# create_subnet
# attach_network_acl
# attach_public_gateway
# detach_public_gateway
# delete_subnet
