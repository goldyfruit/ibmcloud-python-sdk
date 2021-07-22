from ibmcloud_python_sdk.vpc import gateway as ic

# Intentiate the class
gateway = ic.Gateway()

# Retrieve gateway list
gateway.get_public_gateways()

# Retrieve specific gateway (generic)
gateway.get_public_gateway("ibmcloud-pgw-baby")

# Retrieve specific gateway by ID
gateway.get_public_gateway_by_id("r006-351910c5-2c28-4c78-9b36-28da9d4b062a")

# Retrieve specific gateway by name
gateway.get_public_gateway_by_name("ibmcloud-pgw-baby")

# Create gateway
gateway.create_public_gateway(name="cibmcloud-pgw-baby", zone="us-south-3",
                              vpc="r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
                              resource_group="f328f2cdec6d4b4da2844c214dec99")

# Delete gateway
gateway.delete_public_gateway("ibmcloud-pgw-baby")
