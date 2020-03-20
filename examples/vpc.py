#!/usr/bin/env python

from ibmcloud_python_sdk import vpc as ic

# Intentiate the class
vpc = ic.Vpc()

# Retrieve a complete VPC list
vpc.get_vpcs()

# Retrieve specific VPC by ID
vpc.get_vpc_by_id("r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Retrieve specific VPC by name
vpc.get_vpc_by_name("advisory")