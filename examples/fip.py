from ibmcloud_python_sdk.vpc import fip as ic

# Intentiate the class
fip = ic.Fip()

# Retrieve a complete floating IP list
fip.get_floating_ips()

# Retrieve specific floating IP (generic)
fip.get_floating_ip("ibmcloud-fip-baby")

# Retrieve specific floating IP by ID
fip.get_floating_ip_by_id("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Retrieve specific floating IP by name
fip.get_floating_ip_by_name("ibmcloud-fip-baby")

# Retrieve specific floating IP by address
fip.get_floating_ip_by_address("128.128.129.129")

# Create floating IP
fip.reserve_floating_ip(target="0737-968fd5b4-6548-44db-acf0-6ebd6d66a301",
                        name="vm001", zone="us-south-3",
                        resource_group="f328f2cdec6d4b4da2844c214dec9d39")

# Delete floating IP by ID
fip.delete_floating_ip_by_id("0737-968fd5b4-6548-44db-acf0-6ebd6d66a301")

# Delete floating IP by name
fip.delete_floating_ip_by_name("ibmcloud-fip-baby")

# Delete floating IP by using generic delete method
fip.delete_floating_ip("ibmcloud-fip-baby")
