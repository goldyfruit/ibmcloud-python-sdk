#!/usr/bin/env python

from ibmcloud_python_sdk import vpc


# Retrieve a complete VPC list
vpc.get_vpcs()

# Retrieve specific VPC
vpc.get_vpc("r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765")
