from ibmcloud_python_sdk.catalog import catalog_service as cs

# Intentiate the class
catalog = cs.CatalogService()

# Retrieve catalog cloud object storage plans list
catalog.get_cloud_object_storage()

# Retrieve specific catalog cloud object storage plan
catalog.get_requested_object_storage_plan("standard")
