from ibmcloud_python_sdk.vpc import vpc as icv


# Variables
name = 'ibmcloud-vpc-baby'
prefix = 'ibmcloud-vpc-address-prefix-baby'
route = 'ibmcloud-vpc-route-baby'
cidr = '10.1.0.0/16'
zone = 'us-east'
destination = '192.168.8.0/24'
next_hop = '10.0.1.2'

# Intentiate the class
vpc = icv.Vpc()

# Retrieve complete VPC list
vpc.get_vpcs()

# Retrieve specific VPC
vpc.get_vpc(name)

# Retrieve default network ACL information
vpc.get_default_network_acl(name)

# Retrieve default security group information
vpc.get_default_security_group(name)

# Retrieve address prefixes
vpc.get_address_prefixes(name)

# Retrieve specific address prefix
vpc.get_address_prefix(name, prefix)

# Retrieve route list
vpc.get_routes(name)

# Retrieve specific route
vpc.get_route(name, route)

# Create VPC address prefix
vpc.create_address_prefix(name=name, cidr=cidr, zone=zone)

# Create VPC route
vpc.create_route(name=name, destination=destination, zone=zone,
                 next_hop=next_hop)

# Delete VPC
vpc.delete_vpc(name)

# Delete address prefix from VPC
vpc.delete_address_prefix(name, prefix)

# Delete route from VPC
vpc.delete_route(name, route)
