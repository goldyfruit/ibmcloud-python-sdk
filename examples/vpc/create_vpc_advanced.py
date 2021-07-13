"""
This code will first retrieve the ID of the resource group based on a
provided name. Once the information has been retrieved then a VPC will
be created with the current information:
    * With a custom name
    * within the mentioned resource group
    * With a default address prefix
    * With a connection to the classic infrastructure

If classic_access if defined then please read this documentation:
https://ibm.co/3h2cPsi

In case of error: "No valid SoftLayer configuration found", make sure
you only have one classic access per region and read the link from above.
"""
from ibmcloud_python_sdk.vpc import vpc as icv
from ibmcloud_python_sdk.resource import resource_group as icr
import sys


# Variables
vpc_name = 'ibmcloud-vpc-baby'
resource_group_name = 'ibmcloud-resource-group-baby'

# Intentiate classes
vpc = icv.Vpc()
rg = icr.ResourceGroup()

# Retrieve resource group ID and check for error
resource_group_info = rg.get_resource_group(resource_group_name)
if 'errors' in resource_group_info:
    print(resource_group_info['errors'])
    sys.exit()

# Create the VPC based on variable and resource group ID
response = vpc.create_vpc(
            name=vpc_name,
            resource_group=resource_group_info['id'],
            address_prefix_management='auto',
            classic_access=True
        )

# Check for error during the VPC creation process
if 'errors' in response:
    print(response['errors'])
else:
    print(response)
