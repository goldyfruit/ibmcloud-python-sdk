from ibmcloud_python_sdk.vpc import instance as ic

# Intentiate the class
instance = ic.Instance()

# Retrieve a complete instances list
instance.get_instances()

# Retrieve specific instance (generic)
instance.get_instance("ibmcloud-baby")

# Retrieve specific instance by ID
instance.get_instance_by_id("r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Retrieve specific instance by name
instance.get_instance_by_name("ibmcloud-baby")

# Retrieve a complete instance profiles list
instance.get_instance_profiles()

# Retrieve instance profiles
instance.get_instance_profile("mp2-56x448")

# Create an instance
instance.create_instance(name="vm001", profile="cx2-4x8",
                         resource_group="f328f2cdec6d4b4da2844c214dec9d39",
                         vpc="r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
                         image="r006-931515d2-fcc3-11e9-896d-3baa2797200f",
                         pni_subnet="0737-f763775a-05d4-41fb-9da3-3cbd64530",
                         zone="us-south-3")

# Delete instance by ID
instance.delete_instance_by_id("ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Delete instance by name
instance.delete_instance_by_name("vm001")

# Delete instance by using generic delete method
instance.delete_instance("vm001")
