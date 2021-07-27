from ibmcloud_python_sdk.resource import resource_group as ic

# Intentiate the class
resource = ic.ResourceGroup()

# Retrieve resource groups list
resource.get_resource_groups()

# Retrieve specific resource group (generic)
resource.get_resource_group("ibmcloud-rg-baby")

# Retrieve specific resource group by ID
resource.get_resource_group_by_id("f328f2cdec6d4b4da2844c214dec9d39")

# Retrieve specific resource group by name
resource.get_resource_group_by_name("ibmcloud-rg-baby")

# Retrieve resource groups for a specific account
resource.get_resource_groups_by_account("a3d7b8d01e261c24677937c29ab33f3c")
