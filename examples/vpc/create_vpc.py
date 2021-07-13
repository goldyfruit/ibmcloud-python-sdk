"""
This code will create a VPC with the minimum information and handle
possible errors.
"""
from ibmcloud_python_sdk.vpc import vpc as icv


# Variable
vpc_name = 'ibmcloud-vpc-baby'

# Intentiate classe
vpc = icv.Vpc()

# Create the VPC based on variable and resource group ID
response = vpc.create_vpc(name=vpc_name)

# Check for error during the VPC creation process
if 'errors' in response:
    print(response['errors'])
else:
    print(response)
