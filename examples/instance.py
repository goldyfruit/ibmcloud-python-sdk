#!/usr/bin/env python

from ibmcloud_python_sdk import instance as ic

# Intentiate the class
instance = ic.Instance()

# Retrieve a complete instances list
instance.get_instances()

# Retrieve specific instance by ID
instance.get_instance_by_id("r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Retrieve specific instance by name
instance.get_instance_by_name("ibmcloud-baby")
