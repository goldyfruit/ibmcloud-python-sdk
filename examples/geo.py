from ibmcloud_python_sdk.vpc import geo as ic

# Intentiate the class
geo = ic.Geo()

# Retrieve region list
geo.get_regions()

# Retrieve specific region
geo.get_region("us-south")

# Retrieve zones per region
geo.get_region_zones("us-south")

# Retrieve zone per region
geo.get_region_zone("us-south", "us-south-3")
