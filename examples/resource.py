from ibmcloud_python_sdk.vpc import resource as ic

# Intentiate the class
resource = ic.Resource()

# Retrieve a complete resource groups list
resource.get_resource_groups()

# Retrieve resource groups for a specific account
resource.get_resource_groups_by_account("a3d7b8d01e261c24677937c29ab33f3c")
