from ibmcloud_python_sdk.vpc import key as ic

# Intentiate the class
key = ic.Key()

# Retrieve key list
key.get_keys()

# Retrieve specific key (generic)
key.get_key("ibmcloud-key-baby")

# Retrieve specific key by ID
key.get_key_by_id("ea930372-2abd-4aa1-bf8c-3db3ac8cb765")

# Retrieve specific key by name
key.get_key_by_name("ibmcloud-key-baby")

# Create key
key.create_key(name="ibmcloud-key-baby",
               public_key="ssh-rsa AAAAB3NzaC1yc2...",
               type="rsa",
               resource_group="f328f2cdec6d4b4da2844c214dec9d39")

# Delete key
key.delete_key("ibmcloud-key-baby")
