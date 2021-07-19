from ibmcloud_python_sdk.vpc import acl as ica


# Variables
acl_name = 'ibmcloud-network-acl-baby'
rule_name = 'ibmcloud-network-acl-rule-baby'

# Intentiate the class
acl = ica.Acl()

# Retrieve network ACL list
acl.get_network_acls()

# Retrieve specific network ACL
acl.get_network_acl(acl_name)

# Retrieve network ACL rules
acl.get_network_acl_rules(acl_name)

# Retrieve specific network ACL rule
acl.get_network_acl_rule(acl_name, rule_name)

# Delete network ACL
acl.delete_network_acl(acl_name)

# Delete network ACL rule
acl.delete_network_acl_rule(acl_name, rule_name)
