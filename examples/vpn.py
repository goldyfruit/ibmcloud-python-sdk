from ibmcloud_python_sdk.vpc import vpn as ic

# Intentiate the class
vpn = ic.Vpn()

# Variables
gateway = ""

# Retrieve IKE policy list
vpn.get_ike_policies()

# Retrieve specific IKE policy (generic)
vpn.get_ike_policy("ibmcloud-ike-baby")

# Retrieve specific IKE policy by ID
vpn.get_ike_policy_by_id("53ebcf53-2ee4-4a26-ba2c-afc62091a148")

# Retrieve specific IKE policy by name
vpn.get_ike_policy_by_name("ibmcloud-ike-baby")

# Retrieve specific IKE policy connections
vpn.get_ike_policy_connections("ibmcloud-ike-baby")

# Retrieve IPsec policy list
vpn.get_ipsec_policies()

# Retrieve specific IPsec policy (generic)
vpn.get_ipsec_policy("ibmcloud-ipsec-baby")

# Retrieve specific IPsec policy by ID
vpn.get_ipsec_policy_by_id("a4c47690-bc52-45df-9bbd-a1f2b814a8ac")

# Retrieve specific IPsec policy by name
vpn.get_ipsec_policy_by_name("ibmcloud-ipsec-baby")

# Retrieve specific IPsec policy connections
vpn.get_ipsec_policy_connections("ibmcloud-ipsec-baby")

# Retrieve gateway list
vpn.get_gateways()

# Retrieve specific gateway (generic)
vpn.get_gateway("ibmcloud-gateway-baby")

# Retrieve specific gateway by ID
vpn.get_gateway_by_id("e630bb38-c3a7-4619-b0e5-7bff14e060fe")

# Retrieve specific gateway by name
vpn.get_gateway_by_name("ibmcloud-gateway-baby")

# Retrieve connection list for specific gateway
vpn.get_connections("ibmcloud-gateway-baby")

# Retrieve specific connection for specific gateway (generic)
vpn.get_connection("ibmcloud-gateway-baby", "ibmcloud-connection-baby")

# Retrieve specific connection for specific gateway by ID
vpn.get_connection_by_id("ibmcloud-gateway-baby",
                         "b67efb2c-bd17-457d-be8e-7b46404062dc")

# Retrieve specific connection for specific gateway by name
vpn.get_connection_by_name("ibmcloud-gateway-baby",
                           "ibmcloud-connection-baby")

# Retrieve local CIDRs for a specific connection
vpn.get_local_cidrs("ibmcloud-gateway-baby", "ibmcloud-connection-baby")

# Check specific local CIDR for a specific connection
vpn.check_local_cidr("ibmcloud-gateway-baby", "ibmcloud-connection-baby",
                     "10.0.0.0", "24")

# Retrieve peer CIDRs for a specific connection
vpn.get_peer_cidrs("ibmcloud-gateway-baby", "ibmcloud-connection-baby")

# Check specific peer CIDRs for a specific connection
vpn.check_peer_cidr("ibmcloud-gateway-baby", "ibmcloud-connection-baby",
                    "10.0.0.0", "24")

# Create IKE policy
vpn.create_ike_policy(authentication_algorithm="md5", dh_group=2,
                      encryption_algorithm="aes256", ike_version=1,
                      key_lifetime=28800, name="ibmcloud-ike-baby",
                      resource_group="f328f2cdec6d4b4da2844c214dec99")

# Create IPsec policy
vpn.create_ipsec_policy(authentication_algorithm="md5", pfs="disabled",
                        encryption_algorithm="aes256", key_lifetime=28800,
                        name="ibmcloud-ipsec-baby",
                        resource_group="f328f2cdec6d4b4da2844c214dec99")

# Create gateway
vpn.create_gateway(name="ibmcloud-gateway-baby", subnet="ibmcloud-subnet-baby",
                   resource_group="f328f2cdec6d4b4da2844c214dec99")

# Create connection
vpn.create_connection(admin_state_up=True, interval=15, timeout=30,
                      local_cidrs=["192.0.2.50/24"], peer_address="192.0.2.5",
                      ike_policy="ibmcloud-ike-baby", psk="nui24pwraj350SFGWa",
                      ipsec_policy="ibmcloud-ipsec-baby",
                      name="ibmcloud-connection-baby",
                      peer_cidrs=["192.0.2.40/24"])

# Add local CIDR to a connection
vpn.add_local_cidr_connection(gateway="ibmcloud-gateway-baby",
                              connection="ibmcloud-connection-baby",
                              address="10.0.0.0", length="24")

# Add peer CIDR to a connection
vpn.add_peer_cidr_connection(gateway="ibmcloud-gateway-baby",
                             connection="ibmcloud-connection-baby",
                             address="10.0.0.0", length="24")

# Delete IKE policy
vpn.delete_ike_policy("ibmcloud-ike-baby")

# Delete IPsec policy
vpn.delete_ipsec_policy("ibmcloud-ipsec-baby")

# Delete gateway
vpn.delete_gateway("ibmcloud-gateway-baby")

# Delete connection
vpn.delete_connection("ibmcloud-connection-baby")

# Remove local CIDR
vpn.remove_local_cidr("ibmcloud-gateway-baby", "ibmcloud-connection-baby",
                      "10.0.0.0", "24")

# Remove peer CIDR
vpn.remove_peer_cidr("ibmcloud-gateway-baby", "ibmcloud-connection-baby",
                     "10.0.0.0", "24")
