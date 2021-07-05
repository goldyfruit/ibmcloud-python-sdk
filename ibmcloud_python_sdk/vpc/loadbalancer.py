import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import subnet
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Loadbalancer():

    def __init__(self):
        self.cfg = params()
        self.subnet = subnet.Subnet()
        self.rg = resource_group.ResourceGroup()

    def get_lbs(self):
        """Retrieve load balancer list

        :return: List of load balancers
        :rtype: list
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
        """Retrieve specific load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :return: Load balancer information
        :rtype: dict
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
        """Retrieve specific load balancer by ID

        :param id: Load balancer ID
        :type id: str
        :return: Load balancer information
        :rtype: dict
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
        """Retrieve specific load balancer by name

        :param name: Load balancer name
        :type name: str
        :return: Load balancer information
        :rtype: dict
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
        """Retrieve statistics for specific load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :return: Load balancer statistics
        :rtype: dict
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
        """Retrieve listeners for specific load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :return: List of load balancer listeners
        :rtype: list
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
        """Retrieve specific load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :return: Listener information
        :rtype: dict
        """
        by_port = self.get_lb_listener_by_port(lb, listener)
        if "errors" in by_port:
            for key_name in by_port["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_listener_by_id(lb, listener)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_port
        else:
            return by_port

    def get_lb_listener_by_id(self, lb, id):
        """Retrieve specific listener from load balancer by ID

        :param lb: Load balancer name or ID
        :type lb: str
        :param id: Listener ID
        :type id: str
        :return: Listener information
        :rtype: dict
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info
        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}?version={}"
                    "&generation={}".format(lb_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching listener with ID {} from load balancer"
                  " {}. {}".format(id, lb, error))
            raise

    def get_lb_listener_by_port(self, lb, port):
        """Retrieve specific listener from load balancer by port

        :param lb: Load balancer name or ID
        :type lb: str
        :param port: Listener port
        :type port: str
        :return: Listener information
        :rtype: dict
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
                if listener["port"] == port:
                    # Return data
                    return listener

            # Return error if no listener is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching listener with port {} from load balancer"
                  " {}. {}".format(str(port), lb, error))
            raise

    def get_lb_listener_policies(self, lb, listener):
        """Retrieve policies for specific listeners

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :return: List of policies
        :rtype: list
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
        """Retrieve specific policy from listener

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: Policy name or ID
        :type policy: str
        :return: Listerner information
        :rtype: dict
        """
        by_name = self.get_lb_listener_policy_by_name(lb, listener, policy)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_listener_policy_by_id(lb, listener,
                                                              policy)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_lb_listener_policy_by_id(self, lb, listener, id):
        """Retrieve specific policy from listener by ID

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param id: Policy ID
        :type id: str
        :return: Listerner information
        :rtype: dict
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
        """Retrieve specific policy from listener by name

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param name: Policy name
        :type name: str
        :return: Listerner information
        :rtype: dict
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
        """Retrieve rules from listener's policy

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: Policy name or ID
        :type policy: str
        :return: List of rules
        :rtype: list
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
        """Retrieve specific rule from listener's policy

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: Policy name or ID
        :type policy: str
        :param rule: Rule ID
        :type rule: str
        :return: Rule information
        :rtype: dict
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
        """Retrieve pools from loadbalancer

        :param lb: Load balancer name or ID
        :type lb: str
        :return: List of load balancer
        :rtype: list
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools?version={}"
                    "&generation={}".format(lb_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching pools from load balancer {}. {}".format(
                lb, error))
            raise

    def get_lb_pool(self, lb, pool):
        """Retrieve specific pool from load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :return: Pool information
        :rtype: dict
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
        """Retrieve specific pool from load balancer by ID

        :param lb: Load balancer name or ID
        :type lb: str
        :param id: Pool ID
        :type id: str
        :return: Pool information
        :rtype: dict
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}?version={}"
                    "&generation={}".format(lb_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching pool with ID {} from load balancer"
                  " {}. {}".format(id, lb, error))
            raise

    def get_lb_pool_by_name(self, lb, name):
        """Retrieve specific pool from load balancer by name

        :param lb: Load balancer name or ID
        :type lb: str
        :param name: Pool ID
        :type name: str
        :return: Pool information
        :rtype: dict
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
        """Retrieve pools from loadbalancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :return: List of members of a pool
        :rtype: list
        """
        try:
            # Retrieve load balancer information
            lb_info = self.get_lb(lb)
            if "errors" in lb_info:
                return lb_info

            # Retrieve pool information
            pool_info = self.get_lb_pool(lb, pool)
            if "errors" in pool_info:
                return pool_info

            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}/members?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching members from pool {} for load balancer"
                  " {}. {}".format(pool, lb, error))
            raise

    def get_lb_pool_member(self, lb, pool, member):
        """Retrieve specific pool from load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :param member: Member ID
        :type member: str
        :return: Member information
        :rtype: dict
        """
        by_address = self.get_lb_pool_member_by_address(lb, pool, member)
        if "errors" in by_address:
            for key_name in by_address["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_lb_pool_member_by_id(lb, pool, member)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_address
        else:
            return by_address

    def get_lb_pool_member_by_id(self, lb, pool, id):
        """Retrieve specific pool from load balancer by ID

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :param id: Member address or ID
        :type id: str
        :return: Member information
        :rtype: dict
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Retrieve pool information
        pool_info = self.get_lb_pool(lb, pool)
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
            print("Error fetching member with ID {} in pool {} from load"
                  " balancer {}. {}".format(id, pool, lb, error))
            raise

    def get_lb_pool_member_by_address(self, lb, pool, address):
        """Retrieve specific pool from load balancer by ID

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :param address: Member address
        :type address: str
        :return: Member information
        :rtype: dict
        """
        # Retrieve load balancer information
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Retrieve pool information
        pool_info = self.get_lb_pool(lb, pool)
        if "errors" in pool_info:
            return pool_info

        try:
            # Retrieve members
            data = self.get_lb_pool_members(lb_info["id"], pool_info["id"])
            if "errors" in data:
                return data

            # Loop over members until filter match
            for member in data["pools"]:
                if member["name"] == address:
                    # Return data
                    return member

            # Return error if no member is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching member with address {} in pool {} from"
                  " load balancer {}. {}".format(member, pool, lb, error))
            raise

    def create_lb(self, **kwargs):
        """Create load balancer

        :param name: The user-defined name for this load balancer
        :type name: str, optional
        :param subnets: The subnets to provision this load balancer
        :type subnets: list
        :param is_public: The type of this load balancer, public or private
        :type is_public: str
        :param listeners: The listeners of this load balancer
        :type listeners: list, optional
        :param pools: The pools of this load balancer
        :type pools: list, optional
        :param profile: The profile to use for this load balancer
        :type profile: str, optional
        :param resource_group: The resource group for this load balancer
        :type resource_group: str, optional
        """
        args = ["subnets", "is_public"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'subnets': kwargs.get('subnets'),
            'is_public': kwargs.get('is_public'),
            'listeners': kwargs.get('listeners'),
            'pools': kwargs.get('pools'),
            'profile': kwargs.get('profile'),
            'resource_group': kwargs.get('resource_group'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "profile":
                    payload["profile"] = {"name": args["profile"]}
                elif key == "subnets":
                    sb = []
                    for sub in args["subnets"]:
                        tmp_s = {}
                        subnet_info = self.subnet.get_subnet(sub)
                        if "errors" in subnet_info:
                            return subnet_info
                        tmp_s["id"] = subnet_info["id"]
                        sb.append(tmp_s)
                    payload["subnets"] = sb
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "listeners":
                    ln = []
                    for listener in args["listeners"]:
                        ln.append(listener)
                    payload["listeners"] = ln
                elif key == "pools":
                    pl = []
                    for pool in args["pools"]:
                        pl.append(pool)
                    payload["pools"] = pl
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating load balancer. {}".format(error))
            raise

    def create_listener(self, **kwargs):
        """Create listener

        :param lb: Load balancer name or ID
        :type lb: str
        :param certificate_instance: The certificate instance used for SSL
            termination
        :type certificate_instance: str, optional
        :param connection_limit: The connection limit of the listener
        :type connection_limit: int, optional
        :param default_pool: The default pool associated with the listener
        :type default_pool: str, optional
        :param policies: The list of policies of this listener
        :type policies: list, optional
        :param port: The listener port number
        :type port:
        :param protocol: The listener protocol
        :type protocol: str
        """
        args = ["lb", "port", "protocol"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'lb': kwargs.get('lb'),
            'certificate_instance': kwargs.get('certificate_instance'),
            'connection_limit': kwargs.get('connection_limit'),
            'default_pool': kwargs.get('default_pool'),
            'policies': kwargs.get('policies'),
            'port': kwargs.get('port'),
            'protocol': kwargs.get('protocol'),
        }

        # Retrieve load balancer information
        lb_info = self.get_lb(args["lb"])
        if "errors" in lb_info:
            return lb_info

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "lb" and value is not None:
                if key == "certificate_instance":
                    payload["certificate_instance"] = {
                        "crn": args["certificate_instance"]}
                elif key == "default_pool":
                    pool_info = self.get_lb_pool(lb_info["id"],
                                                 args["default_pool"])
                    if "errors" in pool_info:
                        return pool_info
                    payload["default_pool"] = {"id": pool_info["id"]}
                elif key == "policies":
                    pl = []
                    for policy in args["policies"]:
                        pl.append(policy)
                    payload["policies"] = pl
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners?version={}"
                    "&generation={}".format(lb_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating listener in load balancer {}. {}".format(
                lb_info["id"], error))
            raise

    def create_policy(self, **kwargs):
        """Create policy

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param action: The policy action
        :type action: str
        :param name: The user-defined name for this policy
        :type name: str, optional
        :param priority: Priority of the policy
        :type priority: int
        :param rules: The list of rules of this policy
        :type list: list, optional
        :param target: Target depending the action defined
        :type target: str, optional
        """
        args = ["lb", "listener", "action", "priority"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'lb': kwargs.get('lb'),
            'listener': kwargs.get('listener'),
            'action': kwargs.get('action'),
            'name': kwargs.get('name'),
            'priority': kwargs.get('priority'),
            'rules': kwargs.get('rules'),
            'target': kwargs.get('target'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "lb" and key != "listener" and value is not None:
                if key == "rules":
                    rl = []
                    for rule in args["rules"]:
                        rl.append(rule)
                    payload["rules"] = rl
                else:
                    payload[key] = value

        # Retrieve load balancer information
        lb_info = self.get_lb(args["lb"])
        if "errors" in lb_info:
            return lb_info

        # Retrieve listener information
        listener_info = self.get_lb_listener(lb_info["id"], args["listener"])
        if "errors" in listener_info:
            return listener_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies?version={}"
                    "&generation={}".format(lb_info["id"], listener_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating policy for listener {} in load balancer"
                  " {}. {}".format(listener_info["id"], lb_info["id"], error))
            raise

    def create_rule(self, **kwargs):
        """Create rule

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: The policy name or ID
        :type policy: str
        :param condition: The condition of the rule
        :type condition: str
        :param field: HTTP header field
        :type field: str
        :param type: The type of the rule
        :type type: str
        :param value: Value to be matched for rule condition
        :type value: str
        """
        args = ["lb", "listener", "policy", "condition", "type", "value"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'lb': kwargs.get('lb'),
            'listener': kwargs.get('listener'),
            'policy': kwargs.get('policy'),
            'condition': kwargs.get('condition'),
            'field': kwargs.get('field'),
            'type': kwargs.get('type'),
            'value': kwargs.get('value'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if (
                key != "lb"
                and key != "listener"
                and key != "policy"
                and value is not None
            ):
                payload[key] = value

        # Retrieve load balancer information
        lb_info = self.get_lb(args["lb"])
        if "errors" in lb_info:
            return lb_info

        # Retrieve listener information
        listener_info = self.get_lb_listener(lb_info["id"], args["listener"])
        if "errors" in listener_info:
            return listener_info

        # Retrieve policy information
        policy_info = self.get_lb_listener_policy(lb_info["id"],
                                                  listener_info["id"],
                                                  args["policy"])
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}/rules"
                    "?version={}&generation={}".format(lb_info["id"],
                                                       listener_info["id"],
                                                       policy_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating rule for policy {} for listener {} in load"
                  " balancer {}. {}".format(policy_info["id"],
                                            listener_info["id"],
                                            lb_info["id"], error))
            raise

    def create_pool(self, **kwargs):
        """Create pool

        :param lb: Load balancer name or ID
        :type lb: str
        :param algorithm: The load balancing algorithm
        :type algorithm: str
        :param health_monitor: The health monitor of this pool
        :type health_monitor: str
        :param members: The members for this load balancer pool
        :type members: list, optional
        :param name: The user-defined name for this load balancer pool
        :type name: str, optional
        :param protocol: The pool protocol
        :type protocol: str
        :param session_persistence: The session persistence of this pool
        :type session_persistence: str, optional
        """
        args = ["lb", "algorithm", "health_monitor", "protocol"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'lb': kwargs.get('lb'),
            'algorithm': kwargs.get('algorithm'),
            'health_monitor': kwargs.get('health_monitor'),
            'members': kwargs.get('members'),
            'name': kwargs.get('name'),
            'port': kwargs.get('port'),
            'protocol': kwargs.get('protocol'),
            'session_persistence': kwargs.get('session_persistence'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "lb" and value is not None:
                if key == "health_monitor":
                    payload["health_monitor"] = args["health_monitor"]
                elif key == "members":
                    me = []
                    for member in args["members"]:
                        me.append(member)
                    payload["members"] = me
                elif key == "session_persistence":
                    payload["session_persistence"] = args[
                        "session_persistence"]
                else:
                    payload[key] = value

        # Retrieve load balancer information
        lb_info = self.get_lb(args["lb"])
        if "errors" in lb_info:
            return lb_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools?version={}"
                    "&generation={}".format(lb_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating pool in load balancer {}. {}".format(
                lb_info["id"], error))
            raise

    def create_member(self, **kwargs):
        """Create member and add member to the pool

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name or ID
        :type pool: str
        :param port: The port number of the application running in the server
            member
        :type port: int
        :param target: The members for this load balancer pool
        :type target: str
        :param weight: The user-defined name for this load balancer pool
        :type weight: int, optional
        """
        args = ["lb", "pool", "port", "target"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'lb': kwargs.get('lb'),
            'pool': kwargs.get('pool'),
            'port': kwargs.get('port'),
            'target': kwargs.get('target'),
            'weight': kwargs.get('weight'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "lb" and key != "pool" and value is not None:
                if key == "target":
                    payload["target"] = {"address": args["target"]}
                else:
                    payload[key] = value

        # Retrieve load balancer information
        lb_info = self.get_lb(args["lb"])
        if "errors" in lb_info:
            return lb_info

        # Retrieve pool information
        pool_info = self.get_lb_pool(lb_info["id"], args["pool"])
        if "errors" in pool_info:
            return pool_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}/members?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating member into pool {} for load balancer"
                  " {}. {}".format(pool_info["id"], lb_info["id"], error))
            raise

    def delete_lb(self, lb):
        """Delete load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}?version={}&generation={}".format(
                lb_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting load balancer {}. {}".format(lb, error))
            raise

    def delete_listener(self, lb, listener):
        """Delete listener from load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Check if listener exists
        listener_info = self.get_lb_listener(lb_info["id"], listener)
        if "errors" in listener_info:
            return listener_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}?version={}"
                    "&generation={}".format(lb_info["id"], listener_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting listener {} from load balancer {}."
                  " {}".format(listener, lb, error))
            raise

    def delete_policy(self, lb, listener, policy):
        """Delete policy from listener

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: Policy name or ID
        :type policy: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Check if listener exists
        listener_info = self.get_lb_listener(lb_info["id"], listener)
        if "errors" in listener_info:
            return listener_info

        # Check if policy exists
        policy_info = self.get_lb_listener_policy(lb_info["id"],
                                                  listener_info["id"], policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}?version={}"
                    "&generation={}".format(lb_info["id"], listener_info["id"],
                                            policy_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting policy {} in listener {} from load balancer"
                  " {}. {}".format(policy, listener, lb, error))
            raise

    def delete_rule(self, lb, listener, policy, rule):
        """Delete rule from policy

        :param lb: Load balancer name or ID
        :type lb: str
        :param listener: Listener port or ID
        :type listener: str
        :param policy: Policy name or ID
        :type policy: str
        :param rule: Rule ID
        :type rule: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Check if listener exists
        listener_info = self.get_lb_listener(lb_info["id"], listener)
        if "errors" in listener_info:
            return listener_info

        # Check if policy exists
        policy_info = self.get_lb_listener_policy(lb_info["id"],
                                                  listener_info["id"], policy)
        if "errors" in policy_info:
            return policy_info

        # Check if rule exists
        rule_info = self.get_lb_listener_policy_rule(lb_info["id"],
                                                     listener_info["id"],
                                                     policy_info["id"],
                                                     rule)
        if "errors" in rule_info:
            return rule_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/listeners/{}/policies/{}/rules/{}"
                    "?version={}&generation={}".format(lb_info["id"],
                                                       listener_info["id"],
                                                       policy_info["id"],
                                                       rule_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting rule {} from policy {} in listener {} for"
                  " load balancer {}. {}".format(rule, policy, listener, lb,
                                                 error))
            raise

    def delete_pool(self, lb, pool):
        """Delete pool from load balancer

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name ID
        :type pool: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Check if pool exists
        pool_info = self.get_lb_pool(lb_info["id"], pool)
        if "errors" in pool_info:
            return pool_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting pool {} from load balancer {}."
                  " {}".format(pool, lb, error))
            raise

    def delete_member(self, lb, pool, member):
        """Delete member from pool

        :param lb: Load balancer name or ID
        :type lb: str
        :param pool: Pool name ID
        :type pool: str
        :param member: Member address or ID
        :type member: str
        :return: Delete status
        :rtype: dict
        """
        # Check if load balancer exists
        lb_info = self.get_lb(lb)
        if "errors" in lb_info:
            return lb_info

        # Check if pool exists
        pool_info = self.get_lb_pool(lb_info["id"], pool)
        if "errors" in pool_info:
            return pool_info

        # Check if member exists
        member_info = self.get_lb_pool_member(lb_info["id"], pool, member)
        if "errors" in member_info:
            return member_info

        try:
            # Connect to api endpoint for load_balancers
            path = ("/v1/load_balancers/{}/pools/{}/members/{}?version={}"
                    "&generation={}".format(lb_info["id"], pool_info["id"],
                                            member_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting member {} in pool {} from load balancer"
                  " {}. {}".format(member, pool, lb, error))
            raise
