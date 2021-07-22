from ibmcloud_python_sdk.vpc import image as ic

# Intentiate the class
image = ic.Image()

# Retrieve image list
image.get_images()

# Retrieve specific image (generic)
image.get_image("ibmcloud-image-baby")

# Retrieve operating system list
image.get_operating_systems()

# Retrieve specific operating system
image.get_operating_system("ibmcloud-image-baby")

# Retrieve specific image by ID
image.get_image_by_id("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Retrieve specific image by name
image.get_image_by_name("ibmcloud-image-baby")

# Create image
image.create_image(file="cos://us-south/images-bucket/centos8.qcow2",
                   name="ibmcloud-image-baby", operating_system="centos-8",
                   resource_group="f328f2cdec6d4b4da2844c214dec9d39")

# Delete image by ID
image.delete_image_ip_by_id("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Delete image by name
image.delete_image_ip_by_name("ibmcloud-image-baby")

# Delete image by using generic delete method
image.delete_image("ibmcloud-image-baby")
