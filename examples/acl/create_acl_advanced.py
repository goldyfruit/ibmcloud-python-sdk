"""
This code will first retrieve the ID of the resource group based on a
provided name. Once the information has been retrieved then a network ACL
ACL be created and finally a network ACL rule will be added to this network
ACL. The current information will be used:
    * With a custom name
    * within the mentioned resource group
    * With a network ACL rule

The rule will allow inbound traffic on port 80 from any to any.
"""
from ibmcloud_python_sdk.vpc import acl as ica
from ibmcloud_python_sdk.resource import resource_group as icr
import sys


# Variables
vpc_name = 'ibmcloud-vpc-baby'
acl_name = 'ibmcloud-network-acl-baby'
rule_name = 'ibmcloud-network-acl-rule-baby'
resource_group_name = 'ibmcloud-resource-group-baby'

# Intentiate classes
acl = ica.Acl()
rg = icr.ResourceGroup()

# Retrieve resource group ID and check for error
resource_group_info = rg.get_resource_group(resource_group_name)
if 'errors' in resource_group_info:
    print(resource_group_info['errors'])
    sys.exit()

# Create the network ACL based on variables and resource group ID
response_acl = acl.create_network_acl(
            vpc=vpc_name,
            name=acl_name,
            resource_group=resource_group_info['id']
        )

# Check for error during the network ACL creation process
if 'errors' in response_acl:
    print(response_acl['errors'])
else:
    print(response_acl)

# Create the network ACL rule
response_rule = acl.create_network_acl_rule(
            acl=acl_name,
            name=rule_name,
            action='allow',
            source='0.0.0.0/0',
            destinatin='0.0.0.0/0',
            destination_port_min=80,
            destination_port_max=80,
            direction='inbound'
        )

# Check for error during the rule creation process
if 'errors' in response_rule:
    print(response_rule['errors'])
else:
    print(response_rule)
