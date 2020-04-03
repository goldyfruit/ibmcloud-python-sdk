from ibmcloud_python_sdk.vpc import security as ic

# Intentiate the class
security = ic.Security()

# Variables
interface = "0737-968fd5b4-6548-44db-acf0-6ebd6d66a301"
security_group = "2d364f0a-a870-42c3-a554-000001099037"

# Retrieve security group list
security.get_security_groups()

# Retrieve specific security group (generic)
security.get_security_group("ibmcloud-sg-baby")

# Retrieve specific security group by ID
security.get_security_group_by_id(security_group)

# Retrieve specific security group by name
security.get_security_group_by_name("ibmcloud-sg-baby")

# Retrieve network interfaces using a security group
security.get_security_group_interfaces("ibmcloud-sg-baby")

# Retrieve network interfaces using a security group
security.get_security_group_interfaces_by_id(security_group)

# Retrieve network interfaces using a security group
security.get_security_group_interfaces_by_name("ibmcloud-sg-baby")

# Retrieve rule list from security group
security.get_security_group_rules("ibmcloud-sg-baby")

# Retrieve specific rule list from security group
security.get_security_group_rule("ibmcloud-sg-baby",
                                 "r006-c20a8f7c-dee0-48e6-a83c-75e9811863d8")

# Create security group rule
security.create_security_group(name="ibmcloud-sg-baby",
                               vpc="ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
                               resource_group="advisory")

# Create security group rule
security.create_security_group_rule(sg="ibmcloud-sg-baby",
                                    direction="inbound", protocol="tcp",
                                    ip_version="ipv4", port_max=443,
                                    port_min=443, cidr_block="0.0.0.0/0")

# Add network interace to security group
security.add_interface_security_group(security_group="ibmcloud-sg-baby",
                                      interface=interface)

# Remove network interace from security group
security.remove_interface_security_group(security_group="ibmcloud-sg-baby",
                                         interface=interface)

# Delete security group
security.delete_security_group("ibmcloud-sg-baby")

# Delete security group rule
security.delete_security_group_rule("ibmcloud-sg-baby",
                                    "ibmcloud-rule-baby")
