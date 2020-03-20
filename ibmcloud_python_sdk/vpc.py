import http.client
import json
from .config import conn, headers, version, generation


class Vpc():
    # Get all VPC
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/list_vpcs
    # Doc: https://cloud.ibm.com/apidocs/vpc#list-all-vpcs
    def get_vpcs(self):
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


    # Get specific VPC by ID
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-specified-vpc
    def get_vpc_by_id(self, id):
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
            print(f"Error fetching VPC with ID {id}. {error}")
            raise

    # Get specific VPC by name
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-specified-vpc
    def get_vpc_by_name(self, name):
        try:
            # Connect to api endpoint for vpcs
            path = f"/v1/vpcs/?version={version}&generation={generation}"
            conn.request("GET", path, None, headers)

            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Loop over instance until filter match
            for vpc in json.loads(data)['vpcs']:
                if vpc['name'] == name:
                    # Return response data
                    return(vpc)

            # Print and return response data
            return {"vpc": None}

        except Exception as error:
            print(f"Error fetching VPC with name {name}. {error}")
            raise


    # Get VPC default network ACL
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc_default_network_acl
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-a-vpc-s-default-network-acl
    def get_vpc_default_network_acl(self, id):
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
            print(f"Error fetching default network ACL for VPC with ID {id}. {error}")
            raise

    # Get VPC default security group
    # Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_vpc_default_security_group
    # Doc: https://cloud.ibm.com/apidocs/vpc#retrieve-a-vpc-s-default-security-group
    def get_vpc_default_security_group(self, id):
        try:
            # Connect to api endpoint for vpcs
            path = f"/v1/vpcs/{id}/default_security_group?version={version}\
                &generation={generation}"
            conn.request("GET", path, None, headers)

            # Get and read response data
            res = conn.getresponse()
            data = res.read()

            # Print and return response data
            return json.loads(data)

        except Exception as error:
            print(f"Error fetching default security group for VPC with id {id}. {error}")
            raise
