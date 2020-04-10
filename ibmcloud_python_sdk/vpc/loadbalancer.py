import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import subnet
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk import resource_group


class Loadbalancer():

    def __init__(self):
        self.cfg = params()
        self.subnet = subnet.Subnet()
        self.rg = resource_group.Resource()

    def get_lbs(self):
        """
        Retrieve load balancer list
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching load balancers. {}".format(error))
            raise

    def get_lb(self, lb):
        """
        Retrieve specific load balancer
        :param lb: Load balancer name or ID
        """
        by_name = self.get_lb_by_name(lb)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_by_id(lb)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_lb_by_id(self, id):
        """
        Retrieve specific load balancer by ID
        :param id: Load balancer ID
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching load balancer with ID {}. {}".format(
                id, error))
            raise

    def get_lb_by_name(self, name):
        """
        Retrieve specific load balancer by name
        :param name: Load balancer name
        """
        try:
            # Retrieve load balancers
            data = self.get_lbs()
            if "errors" in data:
                return data

            # Loop over load balancers until filter match
            for lb in data["load_balancers"]:
                if lb["name"] == name:
                    # Return data
                    return lb

            # Return error if no load balancer is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching load balancer with name {}. {}".format(
                name, error))
            raise

    def get_lb_stats(self, lb):
        """
        Retrieve statistics for specific load balancer
        :param lb: Load balancer name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/statistics/?version={}"
                    "&generation={}".format(lb_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching statistics for load balancer {}. {}".format(
                lb, error))
            raise

    def get_lb_listeners(self, lb):
        """
        Retrieve listeners for specific load balancer
        :param lb: Load balancer name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners?version={}"
                    "&generation={}".format(lb_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching listeners for load balancer {}. {}".format(
                lb, error))
            raise

    def get_lb_listener(self, lb, listener):
        """
        Retrieve specific load balancer
        :param lb: Load balancer name or ID
        """
        by_name = self.get_lb_listener_by_name(lb, listener)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_listener_by_id(lb, listener)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_lb_listener_by_id(self, lb, id):
        """
        Retrieve specific listener from load balancer by ID
        :param lb: Load balancer name or ID
        :param id: Listener ID
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}?version={}"
                    "&generation={}".format(id, self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching listener with ID {} from load balancer"
                  " {}. {}".format(id, lb, error))
            raise

    def get_lb_listener_by_name(self, lb, name):
        """
        Retrieve specific listener from load balancer by name
        :param lb: Load balancer name or ID
        :param name: Listener name
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        try:
            # Retrieve listeners
            data = self.get_lb_listeners(lb_info["id"])
            if "errors" in data:
                return data

            # Loop over listeners until filter match
            for listener in data["listeners"]:
                if listener["name"] == name:
                    # Return data
                    return listener

            # Return error if no listener is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching listener with name {} from load balancer"
                  " {}. {}".format(name, lb, error))
            raise

    def get_lb_listener_policies(self, lb, listener):
        """
        Retrieve policies for specific listeners
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Retrieve listener information
            listener_info = self.get_lb_listener(lb, listener)
            if "errors" in listener_info:
                return listener_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies?version={}"
                    "&generation={}".format(lb_info["id"], listener_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching policies for listeners {} on load balancer"
                  " {}. {}".format(listener, lb, error))
            raise

    def get_lb_listener_policy(self, lb, listener, policy):
        """
        Retrieve specific policy from listener
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        :param policy: Policy name or ID
        """
        by_name = self.get_lb_listener_policy_by_name(lb, listener)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_listener_policy_by_id(lb, listener)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_lb_listener_policy_by_id(self, lb, listener, id):
        """
        Retrieve specific policy from listener by ID
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        :param id: Policy ID
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}?version={}"
                    "&generation={}".format(lb, listener, id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching policy with ID {} from listener {}"
                  " on load balancer {}. {}".format(id, listener, lb, error))
            raise

    def get_lb_listener_policy_by_name(self, lb, listener, name):
        """
        Retrieve specific policy from listener by name
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        :param name: Policy name
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Retrieve listener information
        listener_info = self.get_lb_listener(lb, listener)
        if "errors" in listener_info:
            return listener_info

        try:
            # Retrieve policies
            data = self.get_lb_listener_policies(lb_info["id"],
                                                 listener_info["id"])
            if "errors" in data:
                return data

            # Loop over policies until filter match
            for policy in data["policies"]:
                if policy["name"] == name:
                    # Return data
                    return policy

            # Return error if no policy is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching policy with name {} from listener {}"
                  " on load balancer {}. {}".format(name, listener, lb, error))
            raise

    def get_lb_listener_policy_rules(self, lb, listener, policy):
        """
        Retrieve rules from listener's policy
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        :param policy: Policy name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Retrieve listener information
            listener_info = self.get_lb_listener(lb, listener)
            if "errors" in listener_info:
                return listener_info

            # Retrieve policy information
            policy_info = self.get_lb_listener_policy(lb, listener, policy)
            if "errors" in policy_info:
                return policy_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}/rules"
                    "?version={}&generation={}".format(lb_info["id"],
                                                       listener_info["id"],
                                                       policy_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rules in policy {} for listeners {} on"
                  " load balancer {}. {}".format(policy, listener, lb, error))
            raise

    def get_lb_listener_policy_rule(self, lb, listener, policy, rule):
        """
        Retrieve specific rule from listener's policy
        :param lb: Load balancer name or ID
        :param listener: Listener name or ID
        :param policy: Policy name or ID
        :param rule: Rule ID
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}/rules/{}"
                    "?version={}&generation={}".format(lb, listener, policy,
                                                       rule,
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rule with ID {} in policy {} from listener"
                  " {} on load balancer {}. {}".format(id, policy, listener,
                                                       lb, error))
            raise

    def get_lb_pools(self, lb):
        """
        Retrieve pools from loadbalancer
        :param lb: Load balancer name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools?version={}"
                    "&generation={}".format(lb_info["id"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching pools from load balancer {}. {}".format(
                lb, error))
            raise

    def get_lb_pool(self, lb, pool):
        """
        Retrieve specific pool from load balancer
        :param lb: Load balancer name or ID
        :param pool: Pool name or ID
        """
        by_name = self.get_lb_pool_by_name(lb, pool)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_pool_by_id(lb, pool)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_lb_pool_by_id(self, lb, id):
        """
        Retrieve specific pool from load balancer by ID
        :param lb: Load balancer name or ID
        :param id: Pool ID
        """
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}?version={}"
                    "&generation={}".format(id, self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching pool with ID {} from load balancer"
                  " {}. {}".format(id, lb, error))
            raise

    def get_lb_pool_by_name(self, lb, name):
        """
        Retrieve specific pool from load balancer by name
        :param lb: Load balancer name or ID
        :param name: Pool name
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        try:
            # Retrieve pools
            data = self.get_lb_pools(lb_info["id"])
            if "errors" in data:
                return data

            # Loop over pools until filter match
            for pool in data["pools"]:
                if pool["name"] == name:
                    # Return data
                    return pool

            # Return error if no pool is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching pool with name {} from load balancer"
                  " {}. {}".format(name, lb, error))
            raise

    def get_lb_pool_members(self, lb, pool):
        """
        Retrieve pools from loadbalancer
        :param lb: Load balancer name or ID
        :param pool: Pool name or ID
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Retrieve pool information
            pool_info = self.get_lb_pool(lb)
            if "errors" in pool_info:
                return pool_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}/members?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching members from pool {} for load balancer"
                  " {}. {}".format(pool, lb, error))
            raise

    def get_lb_pool_member(self, lb, pool, member):
        """
        Retrieve specific pool from load balancer by ID
        :param lb: Load balancer name or ID
        :param pool: Pool name or ID
        :param member: Member ID
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Retrieve pool information
        pool_info = self.get_lb_pool(lb)
        if "errors" in pool_info:
            return pool_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}/members/{}?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"],
                                            id, self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching member {} in pool {} {} from load balancer"
                  " {}. {}".format(id, pool, lb, error))
            raise
