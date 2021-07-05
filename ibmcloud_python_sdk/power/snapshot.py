from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.power import get_power_headers as headers
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.power import instance


class Sanpshot():

    def __init__(self):
        self.cfg = params()
        self.instance = instance.Instance()

    def get_snapshots(self, instance):
        """Retrieve snapshot list for a specific cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :return: List of snapshots
        :rtype: list
        """
        try:
            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/snapshots".format(instance))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching snapshot list for cloud instance {}."
                  " {}".format(instance, error))

    def get_snapshot(self, instance, snapshot):
        """Retrieve specific snapshot by name or by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param snapshot: Snapshot name or ID
        :type snapshot: str
        :return: Snapshot information
        :rtype: dict
        """
        by_name = self.get_snapshot_by_name(instance, snapshot)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_snapshot_by_id(instance, snapshot)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_snapshot_by_id(self, instance, id):
        """Retrieve specific snapshot by ID

        :param instance: Cloud instance ID
        :type instance: str
        :param id: Snapshot ID
        :type id: str
        :return: Snapshot information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for images
            path = ("/pcloud/v1/cloud-instances/{}/snapshots/{}".format(
                instance, id))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching snapshot with ID {} for cloud instance {}."
                  " {}".format(id, instance, error))

    def get_snapshot_by_name(self, instance, name):
        """Retrieve specific snapshot by name

        :param instance: Cloud instance ID
        :type instance: str
        :param name: Snapshot name
        :type name: str
        :return: Snapshot information
        :rtype: dict
        """
        try:
            # Retrieve snapshots
            data = self.get_snapshots(instance)
            if "errors" in data:
                return data

            # Loop over snapshots until filter match
            for snapshot in data['snapshots']:
                if snapshot["name"] == name:
                    # Return data
                    return snapshot

            # Return error if no snapshot is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching snapshot with name {} for cloud instance {}."
                  " {}".format(name, instance, error))

    def delete_snapshot(self, instance, snapshot):
        """Delete cloud instance

        :param instance: Cloud instance ID
        :type instance: str
        :param snapshot: Snapshot name or ID
        :type snapshot: str
        :return: Deletion status
        :rtype: dict
        """
        try:
            # Check if cloud instance exists and retrieve information
            ci_info = self.instance.get_instance(instance)
            if "errors" in ci_info:
                return ci_info

            # Check if snapshot exists and retrieve information
            snap_info = self.get_snapshot(ci_info["name"], snapshot)
            if "errors" in snap_info:
                return snap_info

            # Connect to api endpoint for cloud-instances
            path = ("/pcloud/v1/cloud-instances/{}/snapshot{}".format(
                ci_info["name"], snap_info["snapshotID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting snapshot {} from cloud instance {}."
                  " {}".format(snapshot, instance, error))
