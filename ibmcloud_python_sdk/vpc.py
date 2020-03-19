import http.client
import json
from .config import conn, headers, version, generation


# Get all VPC
# Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/list_vpcs
# Doc: https://cloud.ibm.com/apidocs/vpc#list-all-vpcs
def get_vpcs():
    try:
        # Connect to api endpoint for vpcs
        path = f"/v1/vpcs?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # Print and return response data
        return json.loads(data)

    except Exception as error:
        print(f"Error fetching VPCs. {error}")
        raise


# Get specific VPC
# Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc
# Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-specified-vpc
def get_vpc(id):
    try:
        # Connect to api endpoint for vpcs
        path = f"/v1/vpcs/{id}?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # Print and return response data
        return json.loads(data)

    except Exception as error:
        print(f"Error fetching VPC. {error}")
        raise


# Get VPC default network ACL
# Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc_default_network_acl
# Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-a-vpc-s-default-network-acl
def get_vpc_default_network_acl(id):
    try:
        # Connect to api endpoint for vpcs
        path = f"/v1/vpcs/{id}/default_network_acl?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # Print and return response data
        return json.loads(data)

    except Exception as error:
        print(f"Error fetching VPC default network ACL. {error}")
        raise
