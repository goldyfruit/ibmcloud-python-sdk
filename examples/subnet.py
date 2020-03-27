from ibmcloud_python_sdk.vpc import subnet as ic

# Intentiate the class
subnet = ic.subnet()

# Retrieve a complete subnets list
subnet.get_subnets()

# Retrieve specific subnet (generic)
subnet.get_subnet("ibmcloud-subnet-baby")

# Retrieve specific subnet by ID
subnet.get_subnet_by_id("0737-6364fd95-1573-4178-aaab-285781a5b94c")

# Retrieve specific subnet by name
subnet.get_subnet_by_name("ibmcloud-subnet-baby")

# Create an subnet
subnet.create_subnet(name="ibmcloud-subnet-baby",
                     resource_group="f328f2cdec6d4b4da2844c214dec9d39",
                     vpc="r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
                     total_ipv4_address_count=256, zone="us-south-3")

# Retrieve subnet's network ACL (generic)
subnet.get_subnet_network_acl("ibmcloud-subnet-baby")

# Retrieve subnet's network ACL by ID
subnet.get_subnet_network_acl_by_id(
    "0737-6364fd95-1573-4178-aaab-285781a5b94c")

# Retrieve subnet's network ACL by name
subnet.get_subnet_network_acl_by_name("ibmcloud-subnet-baby")

# Retrieve subnet's public gateway (generic)
subnet.get_subnet_public_gateway("ibmcloud-subnet-baby")

# Retrieve subnet's public gateway by ID
subnet.get_subnet_public_gateway_by_id(
    "0737-6364fd95-1573-4178-aaab-285781a5b94c")

# Retrieve subnet's public gateway by name
subnet.get_subnet_public_gateway_by_name("ibmcloud-subnet-baby")

# Attach network ACL to subnet
na = "hazelnut-rocking-caption-amuser-envoy-comic"
subnet.attach_network_acl(subnet="advisory-net",
                          network_acl=na)

# Attach public gateway to subnet
pg = "pgw-00c6c3c0-6540-11ea-b2cd-53e9ffc40d80"
subnet.attach_public_gateway(subnet="advisory-net",
                             public_gateway=pg)

# Detach gateway from subnet
subnet.detach_public_gateway("advisory-net")

# Delete subnet by ID
subnet.delete_subnet_by_id("0737-6364fd95-1573-4178-aaab-285781a5b94c")

# Delete subnet by name
subnet.delete_subnet_by_name("ibmcloud-subnet-baby")

# Delete subnet by using generic delete method
subnet.delete_subnet("ibmcloud-subnet-baby")
