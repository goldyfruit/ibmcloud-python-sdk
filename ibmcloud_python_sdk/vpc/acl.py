import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk.resource import resource_group


class Acl():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.rg = resource_group.ResourceGroup()

    def get_network_acls(self):
        """Retrieve network ACL list

        :return: List of network ACLs
        :rtype: list
        """
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network ACLs. {}".format(error))
            raise

    def get_network_acl(self, acl):
        """Retrieve specific network ACL

        :param acl: Network ACL name or ID
        :type acl: str
        :return: Network ACL information
        :rtype: dict
        """
        by_name = self.get_network_acl_by_name(acl)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_network_acl_by_id(acl)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_network_acl_by_id(self, id):
        """Retrieve specific network ACL by ID

        :param id: Network ACL ID
        :type id: str
        :return: Network ACL information
        :rtype: dict
        """
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network ACL with ID {}. {}".format(
                id, error))
            raise

    def get_network_acl_by_name(self, name):
        """Retrieve specific network ACL by name

        :param name: Network ACL name
        :type name: str
        :return: Network ACL information
        :rtype: dict
        """
        try:
            # Retrieve network ACLs
            data = self.get_network_acls()
            if "errors" in data:
                return data

            # Loop over network ACLs until filter match
            for acl in data['network_acls']:
                if acl["name"] == name:
                    # Return data
                    return acl

            # Return error if no network ACL is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching network ACL with name {}. {}".format(
                name, error))
            raise

    def get_network_acl_rules(self, acl):
        """Retrieve rules for a specific network ACL

        :param acl: Network ACL
        :type acl: str
        :return: Network ACL rules list
        :rtype: list
        """
        by_name = self.get_network_acl_rules_by_name(acl)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_network_acl_rules_by_id(acl)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_network_acl_rules_by_id(self, id):
        """Retrieve rules for a specific network ACL by ID

        :param id: Network ACL ID
        :type id: str
        :return: Network ACL rules list
        :rtype: dict
        """
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules?version={}"
                    "&generation={}".format(id, self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rules for network ACL with ID"
                  " {}. {}".format(id, error))
            raise

    def get_network_acl_rules_by_name(self, name):
        """Retrieve rules for a specific network ACL by name

        :param name: Network ACL name
        :type name: str
        :return: Network ACL rules list
        :rtype: list
        """
        # Retrieve network ACL information to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(name)
        if "errors" in acl_info:
            return acl_info

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/?version={}"
                    "&generation={}".format(acl_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network ACL with name {}. {}".format(
                name, error))
            raise

    # Get specific network ACL's rule
    def get_network_acl_rule(self, acl, rule):
        """Retrieve specific rule for a specific network ACL

        :param acl: Network ACL name or ID
        :type acl: str
        :param rule: Rule name or ID
        :type rule: str
        :return: Network ACL rule information
        :rtype: dict
        """
        # Retrieve network ACL to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(acl)
        if "errors" in acl_info:
            return acl_info

        by_name = self.get_network_acl_rule_by_name(acl, rule)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_network_acl_rule_by_id(acl, rule)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_network_acl_rule_by_id(self, acl, id):
        """Retrieve specific rule for a specific network ACL by ID

        :param acl: Network ACL name or ID
        :type acl: str
        :param id: Rule ID
        :type id: str
        :return: Network ACL rule information
        :rtype: dict
        """
        # Retrieve network ACL to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(acl)
        if "errors" in acl_info:
            return acl_info

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/{}?version={}"
                    "&generation={}".format(acl_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rule with ID {} for network ACL"
                  "with ID {}. {}".format(id, acl_info["id"], error))
            raise

    def get_network_acl_rule_by_name(self, acl, name):
        """Retrieve specific rule for a specific network ACL by name

        :param acl: Network ACL name or ID
        :type acl: str
        :param name: Rule name
        :type name: str
        :return: Network ACL rule information
        :rtype: dict
        """
        # Retrieve network ACL to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(acl)
        if "errors" in acl_info:
            return acl_info

        try:
            # Retrieve network ACL rules
            data = self.get_network_acl_rules()
            if "errors" in data:
                return data

            # Loop over network ACL rules until filter match
            for rule in data['rules']:
                if rule["name"] == name:
                    # Return data
                    return rule

            # Return error if no network ACL is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching rule with name {} for network ACL"
                  "with ID {}. {}".format(name, acl_info["id"], error))
            raise

    def create_network_acl(self, **kwargs):
        """Create network ACL

        :param name: The unique user-defined name for this network ACL
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param vpc: The VPC the network ACL is to be a part of
        :type vpc: str
        :param rules: Array of prototype objects for rules to create along
            with this network ACL
        :type rules: list, optional
        :param source_network_acl: Network ACL to copy rules from
        :type source_network_acl: str, optional
        """
        args = ["vpc"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'vpc': kwargs.get('vpc'),
            'rules': kwargs.get('rules'),
            'source_network_acl': kwargs.get('source_network_acl'),
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
                    for acl_rules in args["rules"]:
                        rs.append(acl_rules)
                    payload["rules"] = rs
                elif key == "source_network_acl":
                    payload["source_network_acl"] = {
                        "id": args["source_network_acl"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating network ACL. {}".format(error))
            raise

    def create_network_acl_rule(self, **kwargs):
        """Create network ACL rule

        :param name: The unique user-defined name for this network ACL
        :type name: str, optional
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param vpc: The VPC the network ACL is to be a part of
        :type vpc: str
        :param rules: Array of prototype objects for rules to create along
            with this network ACL
        :type rules: list, optional
        """
        args = ["acl", "action", "destination", "direction", "source"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            "acl": kwargs.get('acl'),
            'name': kwargs.get('name'),
            'action': kwargs.get('action'),
            'destination': kwargs.get('destination'),
            'direction': kwargs.get('direction'),
            'source': kwargs.get('source'),
            'before': kwargs.get('before'),
            'protocol': kwargs.get('protocol'),
            'destination_port_max': kwargs.get('destination_port_max'),
            'destination_port_min': kwargs.get('destination_port_min'),
            'source_port_max': kwargs.get('source_port_max'),
            'source_port_min': kwargs.get('source_port_min'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            # acl argument should not be in the payload
            if key != "acl" and value is not None:
                if key == "before":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    payload["resource_group"] = {"id": rg_info["id"]}
                else:
                    payload[key] = value

        # Retrieve network ACL information to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(args["acl"])
        if "errors" in acl_info:
            return acl_info

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules?version={}"
                    "&generation={}".format(acl_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating network ACL rule. {}".format(error))
            raise

    def delete_network_acl(self, acl):
        """Delete network ACL

        :param acl: Network ACL name or ID
        :type acl: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if network ACL exists
            acl_info = self.get_network_acl(acl)
            if "errors" in acl_info:
                return acl_info

            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}?version={}&generation={}".format(
                acl_info["id"], self.cfg["version"], self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting network ACL with {}. {}".format(acl, error))
            raise

    def delete_network_acl_rule(self, acl, rule):
        """Delete network ACL rule

        :param acl: Network ACL name or ID
        :type acl: str
        :param rule: Rule name or ID
        :type rule: str
        :return: Delete status
        :rtype: dict
        """
        try:
            # Check if network ACL and network ACL rule exist
            acl_info = self.get_network_acl(acl)
            if "errors" in acl_info:
                return acl_info

            rule_info = self.get_network_acl_rule(acl_info["id"], rule)
            if "errors" in rule_info:
                return rule_info

            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/{}?version={}"
                    "&generation={}".format(acl_info["id"], rule_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting network ACL rule {} for network"
                  "ACL {}. {}".format(rule, acl, error))
            raise
