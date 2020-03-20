import http.client
import json
from .config import conn, headers, version, generation


# Get all VPC
# Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/list_instances
# Doc: https://cloud.ibm.com/apidocs/instance#list-all-instances
def get_instances():
    try:
        # Connect to api endpoint for instances
        path = f"/v1/instances?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # Print and return response data
        return json.loads(data)

    except Exception as error:
        print(f"Error fetching instances. {error}")
        raise


# Get specific VPC
# Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_instance
# Doc: https://cloud.ibm.com/apidocs/instance#retrieve-specified-instance
def get_instance_by_id(id):
    try:
        # Connect to api endpoint for instance
        path = f"/v1/instances?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        # Print and return response data
        return json.loads(data)

    except Exception as error:
        print(f"Error fetching instance with id {id}. {error}")
        raise

# Get instance by name
def get_instance_by_name(name):
    try:
        # Connect to api endpoint for instance
        path = f"/v1/instances/?version={version}&generation={generation}"
        conn.request("GET", path, None, headers)

        # Get and read response data
        res = conn.getresponse()
        data = res.read()

        for instance in json.loads(data)['instances']: 
            if instance['name'] == name:
                # Return response data
                return(instance)
        # Print and return response data
        return {"instance": None} 

    except Exception as error:
        print(f"Error fetching instances. {error}")
        raise

# create an instance
def create_instance():
    try:
        # Connect to api endpoint for instances
        path = f"/v1/instances?version={version}&generation={generation}"
        body = {}
        conn.request("PUT", path, body, headers)
    except Exception as error:
        print(f"Error fetching instances. {error}")
        raise
## Get VPC default network ACL
## Spec: https://pages.github.ibm.com/riaas/api-spec/spec_aspirational/#/VPCs/get_instance_default_network_acl
## Doc: https://cloud.ibm.com/apidocs/instance#retrieve-a-instance-s-default-network-acl
#def get_instance_default_network_acl(id):
#    try:
#        # Connect to api endpoint for instances
#        path = f"/v1/instances/{id}/default_network_acl?version={version}&generation={generation}"
#        conn.request("GET", path, None, headers)
#
#        # Get and read response data
#        res = conn.getresponse()
#        data = res.read()
#
#        # Print and return response data
#        return json.loads(data)
#
#    except Exception as error:
#        print(f"Error fetching VPC default network ACL. {error}")
#        raise
