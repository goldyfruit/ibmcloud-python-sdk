from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_not_found


class CatalogService():

    def __init__(self):
        self.cfg = params()

    def get_cloud_object_storage(self):
        """Retrieve cloud object storage list

        :return: List of cloud object storage
        "rtype: list
        """
        try:
            # Connect to api endpoint for cloud-object-storage
            path = "/api/v1?q=cloud-object-storage"

            # Return data
            return qw("gc", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching cloud object storage. {}".format(error))
            raise

    def get_cloud_object_storage_id(self):
        """Retrieve cloud object storage id

        :return: String of cloud object storage id
        :rtype: str
        """
        try:
            cloud_obj_storage = self.get_cloud_object_storage()
            if "errors" in cloud_obj_storage:
                return cloud_obj_storage

            for cloud_object in cloud_obj_storage["resources"]:
                if cloud_object['children'][0]['id']:
                    return cloud_object['children'][0]['id']

            return resource_not_found()

        except Exception as error:
            print("Error fetching object storage id. {}". format(
                error))
            raise

    def get_object_storage_plans(self):
        """Retrieve object storage plans

        :return: List of cloud storage plans
        :rtype: list
        """
        storage_id = self.get_cloud_object_storage_id()

        try:
            # Connect to api endpoint of defined storage plan
            path = "/api/v1/{}/plan".format(storage_id)

            # Return data
            return qw("gc", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching storage plan. {}".format(error))
            raise

    def get_requested_object_storage_plan(self, plan_name):
        """Retrieve defined object storage plan

        :return: Dictionary of selected storage plan
        :rtype: dict
        """
        try:
            storage_plans = self.get_object_storage_plans()
            if "errors" in storage_plans:
                return storage_plans

            for storage_plan in storage_plans["resources"]:
                if storage_plan["name"] == plan_name:
                    return storage_plan

            return resource_not_found()

        except Exception as error:
            print("Error fetching requested storage plan {}. {}".format(
                plan_name, error))
            raise
