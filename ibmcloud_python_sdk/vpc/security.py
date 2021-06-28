import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group
from ibmcloud_python_sdk.vpc import instance


class Security():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.rg = resource_group.ResourceGroup()
        self.instance = instance.Instance()

    def get_security_groups(self):
        """Retrieve security group list

        :return: List of security groups
        :rtype: list
        """
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching security groups. {}".format(error))
            raise

    def get_security_group(self, security_group):
        """Retrieve specific security group

        :param security_group: Security group name or ID
        :type security_group: str
        :return: Security group information
        :rtype: dict
        """
        by_name = self.get_security_group_by_name(security_group)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_security_group_by_id(security_group)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_security_group_by_id(self, id):
        """Retrieve specific security group by ID

        :param id: Security group ID
        :type id: str
        :return: Security group information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching security group with ID {}. {}".format(
                id, error))
            raise

    def get_security_group_by_name(self, name):
        """Retrieve specific security group by name

        :param name: Security group name
        :type name: str
        :return: Security group information
        :rtype: dict
        """
        try:
            # Retrieve security groups
            data = self.get_security_groups()
            if "errors" in data:
                return data

            # Loop over security groups until filter match
            for sg in data['security_groups']:
                if sg["name"] == name:
                    # Return data
                    return sg

            # Return error if no security group is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching security group with name {}. {}".format(
                name, error))
            raise

    def get_security_group_interfaces(self, security_group):
        """Retrieve network interfaces associated to a security group

        :param security_group: Security group name or ID
        :type security_group: str
        :return: List of network interfaces
        :rtype: list
        """
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces?version={}"
                    "&generation={}".format(sg_info["id"], self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces associated to security"
                  " group {}. {}".format(security_group, error))
            raise

    def get_security_group_interface(self, security_group, interface):
        """Retrieve specific network interface associated to a security group

        :param security_group: Security group name or ID
        :type security_group: str
        :param interface: Network interface name or ID
        :type interface: str
        :return: Network interface information
        :rtype: dict
        """
        by_name = self.get_security_group_interface_by_name(security_group,
                                                            interface)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_security_group_interface_by_id(
                        security_group, interface)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_security_group_interface_by_id(self, security_group, id):
        """Retrieve specific network interface associated to a security group
        by ID

        :param security_group: Security group name or ID
        :type security_group: str
        :param id: Network interface ID
        :type id: str
        :return: Network interface information
        :rtype: dict
        """
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces/{}?version={}"
                    "&generation={}".format(sg_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interface with ID {} associated to"
                  " security group {}. {}".format(id, security_group, error))
            raise

    def get_security_group_interface_by_name(self, security_group, name):
        """Retrieve specific network interface associated to a security group
        by name

        :param security_group: Security group name or ID
        :type security_group: str
        :param name: Network interface name
        :type name: str
        :return: Network interface information
        :rtype: dict
        """
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Retrieve network interfaces
            data = self.get_security_group_interfaces(sg_info["id"])
            if "errors" in data:
                return data

            # Loop over network interfaces until filter match
            for nic in data['network_interfaces']:
                if nic["name"] == name:
                    # Return data
                    return nic

            # Return error if no interface is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching network interface with name {} associated to"
                  " security group {}. {}".format(name, security_group, error))
            raise

    def get_security_group_rules(self, security_group):
        """Retrieve rules from a security group

        :param security_group: Security group name or ID
        :type security_group: str
        :return: List of rules
        :rtype: list
        """
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules?version={}"
                    "&generation={}".format(sg_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rules for security group with"
                  " ID {}. {}".format(id, error))
            raise

    def get_security_group_rule(self, security_group, rule):
        """Retrieve specific rule from a security group

        :param security_group: Security group name or ID
        :type security_group: str
        :param rule: Rule ID
        :type rule: str
        :return: Rule information
        :rtype: dict
        """
        by_id = self.get_security_group_rule_by_id(security_group, rule)
        if "errors" in by_id:
            return by_id

        return by_id

    def get_security_group_rule_by_id(self, security_group, id):
        """Retrieve specific rule from a security group by ID

        :param security_group: Security group name or ID
        :type security_group: str
        :param id: Rule ID
        :type id: str
        :return: Rule information
        :rtype: dict
        """
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules/{}?version={}"
                    "&generation={}".format(sg_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rule with ID {} for security group"
                  " {}. {}".format(id, security_group, error))
            raise

    def add_interface_security_group(self, **kwargs):
        """Add network interface to a security group

        :param interface: The network interface ID
        :type interface: str
        :param security_group: The security group name or ID
        :type security_group: str
        :param instance: Instance name or ID
        :type instance: str, optional
        """
        args = ["interface", "security_group"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'interface': kwargs.get('interface'),
            'security_group': kwargs.get('security_group'),
            'instance': kwargs.get('instance'),
        }

        target = args["interface"]

        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(args["security_group"])
        if "errors" in sg_info:
            return sg_info

        if args["instance"]:
            # Retrieve network interface information to get the ID
            # (mostly useful if a name is provided)
            nic_info = self.instance.get_instance_interface(
                args["instance"], args["interface"])
            if "errors" in nic_info:
                return nic_info
            target = nic_info["id"]

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces/{}?version={}"
                    "&generation={}".format(sg_info["id"],
                                            target,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "PUT", path, headers(), None)["data"]

        except Exception as error:
            print("Error adding network interface {} to security group"
                  " {}. {}".format(target, args["security_group"], error))
            raise

    def create_security_group(self, **kwargs):
        """Create security group

        :param name: The user-defined name for this security group
        :type name: str, optional
        :param resource_group: The resource group to use
        :type security_group: str, optional
        :param vpc: The VPC this security group is to be a part of
        :type vpc: str
        :param rules: Array of rule prototype objects for rules to be created
            for this security group
        :type rules: list, optional
        """
        args = ["vpc"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'vpc': kwargs.get('vpc'),
            'rules': kwargs.get('rules'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "vpc":
                    vpc_info = self.vpc.get_vpc(args["vpc"])
                    if "errors" in vpc_info:
                        return vpc_info
                    payload["vpc"] = {"id": vpc_info["id"]}
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "rules":
                    rs = []
                    for sg_rules in args["rules"]:
                        rs.append(sg_rules)
                    payload["rules"] = rs
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating security group. {}".format(error))
            raise

    def create_security_group_rule(self, **kwargs):
        """Create security group rule

        :param sg: Security group name or ID where to add the rule
        :type sg: str
        :param direction: The direction of traffic to enforce, either inbound
            or outbound
        :type direction: str
        :param ip_version: The IP version to enforce
        :type ip_version: str
        :param protocol: The protocol to enforce
        :type protocol: str
        :param port_min: The inclusive lower bound of TCP/UDP port range
        :type port_min: int
        :param port_max: The inclusive upper bound of TCP/UDP port range
        :type port_max: int
        :param code: The ICMP traffic code to allow
        :type code: int
        :param type: The ICMP traffic type to allow
        :type type: str
        :param cidr_block: The CIDR block
        :type cidr_block: str
        :param address: The IP address
        :type address: str
        :param security_group: The unique identifier for this security group
        :type security_group: str
        """
        args = ["sg", "direction"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            "sg": kwargs.get('sg'),
            'direction': kwargs.get('direction'),
            'ip_version': kwargs.get('ip_version'),
            'protocol': kwargs.get('protocol'),
            'port_min': kwargs.get('port_min'),
            'port_max': kwargs.get('port_max'),
            'code': kwargs.get('code'),
            'type': kwargs.get('type'),
            'cidr_block': kwargs.get('cidr_block'),
            'address': kwargs.get('address'),
            'security_group': kwargs.get('security_group'),
        }

        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(args["sg"])
        if "errors" in sg_info:
            return sg_info

        # Construct payload
        payload = {}
        for key, value in args.items():
            # sg argument should not be in the payload
            if key != "sg" and value is not None:
                if key == "security_group":
                    payload["remote"] = {"id": sg_info["id"]}
                elif key == "address":
                    payload["remote"] = {"address": args["address"]}
                elif key == "cidr_block":
                    payload["remote"] = {"cidr_block": args["cidr_block"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules?version={}"
                    "&generation={}".format(sg_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating security group rule. {}".format(error))
            raise

    def delete_security_group(self, security_group):
        """Delete security group

        :param security_group: Security group name or ID
        :type security_group: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if security group exists
            sg_info = self.get_security_group_by_name(security_group)
            if "errors" in sg_info:
                return sg_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}?version={}&generation={}".format(
                sg_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting security group {}. {}".format(
                security_group, error))
            raise

    def remove_interface_security_group(self, security_group, interface):
        """Remove network interface from a security group

        :param security_group: Security group name or ID
        :type security_group: str
        :parem interface: Interface ID
        :type interface: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if security group exists
            sg_info = self.get_security_group(security_group)
            if "errors" in sg_info:
                return sg_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces/{}?version={}"
                    "&generation={}".format(sg_info["id"], interface,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error removing network interface {} from security group"
                  " {}. {}".format(interface, security_group, error))
            raise

    def delete_security_group_rule(self, security_group, rule):
        """Delete rule from security group

        :param security_group: Security group name or ID
        :type security_group: str
        :parem rule: Rule name or ID
        :type rule: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if security group exists
            sg_info = self.get_security_group(security_group)
            if "errors" in sg_info:
                return sg_info

            # Check if rule exists
            rule_info = self.get_security_group_rule(sg_info["id"], rule)
            if "errors" in rule_info:
                return rule_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules/{}?version={}"
                    "&generation={}".format(sg_info["id"], rule_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting rule {} from security group {}. {}".format(
                rule, security_group, error))
            raise
