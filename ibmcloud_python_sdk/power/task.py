from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.power import get_power_headers as headers


class Task():

    def __init__(self):
        self.cfg = params()

    def get_task(self, task):
        """Retrieve specific task

        :param task: Task ID
        :type task: str
        :return: Task information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for tasks
            path = ("/pcloud/v1/tasks/{}".format(task))

            # Return data
            return qw("power", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching task {}. {}".format(task, error))

    def delete_task(self, task):
        """Delete task

        :param task: Task ID
        :type task: str
        :return: Deletion status
        :rtype: dict
        """
        # Check if task exists and get information
        task_info = self.get_task(task)
        if "errors" in task_info:
            return task_info

        try:
            # Connect to api endpoint for tasks
            path = ("/pcloud/v1/tasks/{}".format(task_info["taskID"]))

            data = qw("power", "DELETE", path, headers())

            # Return data
            if data["response"].status != 200:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting task {}. {}".format(task, error))
