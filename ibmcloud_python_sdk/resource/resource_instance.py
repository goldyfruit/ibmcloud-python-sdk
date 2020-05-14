import json
import re
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.resource import resource_group
from ibmcloud_python_sdk.utils.common import check_args
from urllib.parse import quote


class ResourceInstance():

    def __init__(self):
        self.cfg = params()
        self.rg = resource_group.ResourceGroup()
        self.resource_plan_dict = {"dns": "dc1460a6-37bd-4e2b-8180-d0f86ff39baa", 
                        "object-storage": "2fdf0c08-2d32-4f46-84b5-32e0c92fffd8"}
        #   ibmcloud catalog service-marketplace  | grep cloud-object-storage
        #   ibmcloud catalog service dff97f5c-bc5e-4455-b470-411c3edbe49c

    def create_resource_instance(self, **kwargs):
        """Create resource instance

        :param: name: The name of the instance.
        :param: resource_group: Short or long ID of resource group.
        :param: resource_plan: The unique ID of the plan associated with the
            offering. This value is provided by and stored in the global
            catalog.
        :param: target: The deployment location where the instance should
            be hosted.
        :param: tags: Optional. Tags that are attached to the instance after
            provisioning.
        :param: allow_cleanup: Optional. TA boolean that dictates if the
            resource instance should be deleted (cleaned up) during the
            processing of a region instance delete call.
        :param: parameters: Optional. Configuration options represented as
            key-value pairs that are passed through to the target resource
            brokers.
        :return Resource instance information
        :rtype dict
        """
        args = ['name', 'resource_group', 'resource_plan']
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'resource_plan': kwargs.get('resource_plan'),
            'tags': kwargs.get('tags'),
            'allow_cleanup': kwargs.get('allow_cleanup', False),
            'parameters': kwargs.get('parameters'),
            'target': kwargs.get('target', 'bluemix-global'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_plan":
                    rp_info = self.get_resource_plan(args['resource_plan'])
                    if "errors" in rp_info:
                        return rp_info
                    payload["resource_plan_id"] = rp_info
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = rg_info["id"]
                elif key == "tags":
                    tg = []
                    for tag in args["tags"]:
                        tg.append(tag)
                    payload["tags"] = tg
                elif key == "parameters":
                    payload["parameters"] = args['parameters']
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for resource_instances
            path = ("/v2/resource_instances")

            return qw("rg", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating resource instance. {}".format(error))

    def get_resource_plan(self, resource_plan):
        """Return resource_plan_id based on the input

        :param resource_plan: Required. Resource plan Name or ID
        """
        # if ressource_plan is an id, return the id
        regex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        result = re.compile(regex)

        # if resource_plan match the regexp, return ressource_plan
        if result.search(resource_plan):
            return resource_plan
        elif resource_plan in self.resource_plan_dict:
            return self.resource_plan_dict[resource_plan]

    def get_resource_instances(self, resource_group=None):
        """Retrieve resource instance list

        :param resource_group: Optional. Filter resource instance by resource
        group.
        :return Resource instance list
        :rtype dict
        """
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances?type=service_instance")
            if resource_group:
                path = ("/v2/resource_instances?resource_group={}"
                        "&type=service_instance".format(resource_group))

            return qw("rg", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching resource instances. {}".format(error))
            raise

    def get_resource_instance(self, resource_instance):
        """ Retrieve specific resource instance by name or by ID

        :param resource_instance: Resource instance name or ID
        :return Resource instance information
        :rtype dict
        """
        by_name = self.get_resource_instance_by_name(resource_instance)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_guid = self.get_resource_instance_by_guid(
                        resource_instance)
                    if "errors" in by_guid:
                        return by_guid
                    return by_guid
                else:
                    return by_name
        else:
            return by_name

    def get_resource_instance_by_guid(self, guid):
        """Retrieve specific resoure instance by GUID

        :param guid: Resource instance GUID
        :return Resource instance information
        :rtype dict
        """
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances/{}".format(quote(guid)))

            result = qw("rg", "GET", path, headers())["data"]

            if "status_code" in result:
                if result["status_code"] == 404:
                    return resource_not_found()
                return result

            return result
        except Exception as error:
            print("Error fetching resource instance with ID {}. {}".format(
                guid, error))
            raise

    def get_resource_instance_by_name(self, name):
        """Retrieve specific resoure instance by name

        :param name: Resource instance name
        :return Resource instance information
        :rtype dict
        """
        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances?name={}".format(quote(name)))

            resource_instance = qw("rg", "GET", path, headers())["data"]
            if len(resource_instance["resources"]) == 0:
                return resource_not_found()

            return resource_instance["resources"][0]
        except Exception as error:
            print("Error fetching resource instances with name {}. {}".format(
                name, error))
            raise

    def delete_resource_instance(self, instance):
        """Delete a resource instance

        :param: instance: required. The resource instance id or name
        """
        try:
            instance = self.get_resource_instance(instance)
            if "errors" in instance:
                for key in instance["errors"]:
                    if key["code"] == "not_found":
                       return resource_not_found()
                    else:
                        return instance
            else:
                guid = instance["guid"]
        except Exception as error:
            print("Error finding instance. {}".format(error))
            raise

        try:
            # Connect to api endpoint for resource instances
            path = ("/v2/resource_instances/{}".format(guid))
            result =  qw("rg", "DELETE", path, headers())
        
            if result["data"] == None:
                if result["response"].getcode() == 204:
                    return({"message": "deletion request successfully initiated"})
                else:
                    return result

        except Exception as error:
            print("Error deleting resource instance. {}".format(error))
            raise