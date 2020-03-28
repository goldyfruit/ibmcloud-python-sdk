from ibmcloud_python_sdk.vpc import acl as ic

# Intentiate the class
acl = ic.Acl()

# Retrieve a complete network ACL list
acl.get_network_acls()

# Retrieve specific network ACL (generic)
acl.get_network_acl("ibmcloud-acl-baby")

# Retrieve specific network ACL by ID
acl.get_network_acl_by_id("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Retrieve specific network ACL by name
acl.get_network_acl_by_name("ibmcloud-acl-baby")

# Retrieve network ACL rules (generic)
acl.get_network_acl_rules("ibmcloud-acl-baby")

# Retrieve network ACL rules by ID
acl.get_network_acl_rules_by_id("r006-39bae76f-52fd-41e0-93eb-49861a2a4f23")

# Retrieve network ACL rules by name
acl.get_network_acl_rules_by_name("ibmcloud-acl-baby")

# Retrieve specific network ACL rule (generic)
acl.get_network_acl_rule("ibmcloud-acl-baby", "ibmcloud-acl-rule-baby")

# Retrieve specific network ACL rule by ID
acl.get_network_acl_rule_by_id("ibmcloud-acl-baby",
                               "a3eecc9e-6667-4094-bf3e-9e0c5020186f")

# Retrieve specific network ACL rule by name
acl.get_network_acl_rule_by_name("ibmcloud-acl-baby", "ibmcloud-acl-rule-baby")

# Create network ACL
acl.create_network_acl(name="vm001",
                       vpc="r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
                       resource_group="f328f2cdec6d4b4da2844c214dec9d39")

# Create network ACL rule
acl.create_network_acl_rule(acl="ibmcloud-acl-baby",
                            action="allow",
                            destination="0.0.0.0/0",
                            destination_port_min=80,
                            destination_port_max=80,
                            direction="inbound",
                            protocol="tcp",
                            source="0.0.0.0/0")

# Delete network ACL (generic)
acl.delete_network_acl("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Delete network ACL by ID
acl.delete_network_acl_by_id("ibmcloud-fip-baby")

# Delete network ACL by name
acl.delete_network_acl_by_name("ibmcloud-fip-baby")

# Delete network ACL rule
acl.delete_network_acl_rule("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Delete network ACL rule by ID
acl.delete_network_acl_rule_by_id("ibmcloud-fip-baby")

# Delete network ACL rule by name
acl.delete_network_acl_rule_by_name("ibmcloud-fip-baby")
