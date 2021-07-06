from ibmcloud_python_sdk.vpc import vpc as ic

# Intentiate the class
vpc = ic.Vpc()

# Retrieve a complete VPC list
vpc.get_vpcs()

# Retrieve specific VPC (generic)
vpc.get_vpc("ibmcloud-vpc-baby")

# Retrieve specific VPC by ID
vpc.get_vpc_by_id("r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Retrieve specific VPC by name
vpc.get_vpc_by_name("advisory")

# Create VPC
vpc.create_vpc(name="ibmcloud-vpc-baby",
               resource_group="f328f2cdec6d4b4da2844c214dec9d39")

# Delete VPC
vpc.delete_vpc("ibmcloud-vpc-baby")
