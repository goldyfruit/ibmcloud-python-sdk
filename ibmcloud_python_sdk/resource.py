import http.client
import json
from .config import conn_rg, headers, version, generation

class Resource():
    # Get all resource groups
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/list_instances
    def get_resource_groups(self):
        try:
            # Connect to api endpoint for resource_groups
            path = "/v2/resource_groups"
            conn_rg.request("GET", path, None, headers)

            # Get and read response data
            res = conn_rg.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching resource groups. {error}")
            raise


    # Get resource groups by account
    # Doc: https://cloud.ibm.com/apidocs/resource-controller/resource-manager#get-a-list-of-all-resource-groups
    def get_resource_groups_by_account(self, id):
        try:
            # Connect to api endpoint for resource_groups
            path = f"/v2/resource_groups?account_id={id}"
            conn_rg.request("GET", path, None, headers)

            # Get and read response data
            res = conn_rg.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching resource groups for account {id}. {error}")
            raise
