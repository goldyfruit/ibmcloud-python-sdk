from ibmcloud_python_sdk.vpc import volume as ic

# Intentiate the class
volume = ic.Volume()

# Retrieve volume list
volume.get_volumes()

# Retrieve specific volume (generic)
volume.get_volume("ibmcloud-volume-baby")

# Retrieve volume profile list
volume.get_volume_profiles()

# Retrieve specific volume profile
volume.get_volume_profile("ibmcloud-db-iops")

# Retrieve specific volume by ID
volume.get_volume_by_id("r006-d01c7629-fdbb-41e2-8342-9e7d89184af7")

# Retrieve specific volume by name
volume.get_volume_by_name("ibmcloud-volume-baby")

# Create volume
volume.create_volume(name="gtrellu-sdk", iops=3000,
                     resource_group="f328f2cdec6d4b4da2844c214dec9d39",
                     profile="general-purpose", capacity=100,
                     zone="us-south-3")

# Delete volume
volume.delete_volume("ibmcloud-volume-baby")
