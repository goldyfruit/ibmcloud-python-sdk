import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Acl():

    def __init__(self):
        self.cfg = params()

    # Get all network ACLs
    def get_network_acls(self):
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching network ACLs. {error}")
            raise

    # Get specific network ACL
    # This method is generic and should be used as prefered choice
    def get_network_acl(self, acl):
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

    # Get specific network ACL by ID
    def get_network_acl_by_id(self, id):
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching network ACL with ID {id}. {error}")
            raise

    # Get specific network ACL by name
    def get_network_acl_by_name(self, name):
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve network ACL data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over network ACLs until filter match
            for acl in data['network_acls']:
                if acl["name"] == name:
                    # Return data
                    return acl

            # Return error if no network ACL is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching network ACL with name {name}. {error}")
            raise

    # Get network ACL rules
    # This method is generic and should be used as prefered choice
    def get_network_acl_rules(self, acl):
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

    # Get network ACL's rules by ID
    def get_network_acl_rules_by_id(self, id):
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rules for network ACL"
                  "with ID {}. {}").format(id, error)
            raise

    # Get network ACL's rules by name
    def get_network_acl_rules_by_name(self, name):
        # Retrieve network ACL information to get the ID
        # (mostly useful if a name is provided)
        network_acl = self.get_network_acl(name)
        if "errors" in network_acl:
            return network_acl

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/?version={}"
                    "&generation={}").format(network_acl["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching network ACL with name {name}. {error}")
            raise

    # Get specific network ACL's rule
    def get_network_acl_rule(self, acl, rule):
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

    # Get specific network ACL's rule by id
    def get_network_acl_rule_by_id(self, acl, id):
        # Retrieve network ACL to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(acl)
        if "errors" in acl_info:
            return acl_info

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/{}?version={}"
                    "&generation={}").format(acl_info["id"], id,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rule with ID {} for network ACL"
                  "with ID {}. {}").format(id, acl_info["id"],
                                           error)
            raise

    # Get specific network ACL's rule by name
    def get_network_acl_rule_by_name(self, acl, name):
        # Retrieve network ACL to get the ID
        # (mostly useful if a name is provided)
        acl_info = self.get_network_acl(acl)
        if "errors" in acl_info:
            return acl_info

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules?version={}"
                    "&generation={}").format(acl_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Retrieve network ACL rules data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over network ACL rules until filter match
            for rule in data['rules']:
                if rule["name"] == name:
                    # Return data
                    return rule

            # Return error if no VPC is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print("Error fetching rule with name {} for network ACL"
                  "with ID {}. {}").format(name, acl_info["id"],
                                           error)
            raise

    # Create network ACL
    def create_network_acl(self, **kwargs):
        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'vpc': kwargs.get('vpc'),
            'rules': kwargs.get('rules'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key == "vpc":
                if value is not None:
                    payload["vpc"] = {"id": args["vpc"]}
            elif key == "resource_group":
                if value is not None:
                    payload["resource_group"] = {"id": args["resource_group"]}
            elif key == "rules":
                if value is not None:
                    rs = []
                    for acl_rules in args["rules"]:
                        tmp = {}
                        tmp["id"] = acl_rules
                        rs.append(tmp)
                    payload["rules"] = rs
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating network ACL. {error}")
            raise

    # Create network ACL rule
    def create_network_acl_rule(self, **kwargs):
        # Required parameters
        required_args = set(["acl"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )
        # Set default value is not required paramaters are not defined
        args = {
            "acl": kwargs.get('acl'),
            'name': kwargs.get('name'),
            'action': kwargs.get('action'),
            'destination': kwargs.get('destination'),
            'direction': kwargs.get('direction'),
            'source': kwargs.get('source'),
            'before': kwargs.get('before'),
            'protocol': kwargs.get('protocol'),
            'destidestination_port_maxation': kwargs.get(
                'destidestination_port_maxation'),
            'destination_port_min': kwargs.get('destination_port_min'),
            'source_port_max': kwargs.get('dessource_port_maxtination'),
            'source_port_min': kwargs.get('source_port_min'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            # acl argument should not be in the payload
            if key != "acl" and value is not None:
                if key == "before":
                    payload["before"] = {"id": args["resource_group"]}
                else:
                    payload[key] = value

        # Retrieve network ACL information to get the ID
        # (mostly useful if a name is provided)
        acl = self.get_network_acl(args["acl"])

        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules?version={}"
                    "&generation={}").format(acl["id"], self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating network ACL rule. {error}")
            raise

    # Delete network ACL
    # This method is generic and should be used as prefered choice
    def delete_network_acl(self, acl):
        by_name = self.delete_network_acl_by_name(acl)
        if "errors" in by_name:
            for key_vpc in by_name["errors"]:
                if key_vpc["code"] == "not_found":
                    by_id = self.delete_network_acl_by_id(acl)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete network ACL by ID
    def delete_network_acl_by_id(self, id):
        try:
            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting network ACL with id {id}. {error}")
            raise

    # Delete network ACL by name
    def delete_network_acl_by_name(self, name):
        try:
            # Check if network ACL exists
            acl = self.get_network_acl_by_name(name)
            if "errors" in acl:
                return acl

            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}?version={}&generation={}").format(
                acl["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting network ACL with name {name}. {error}")
            raise

    # Delete network ACL rule
    # This method is generic and should be used as prefered choice
    def delete_network_acl_rule(self, acl, rule):
        by_name = self.delete_network_acl_rule_by_name(acl, rule)
        if "errors" in by_name:
            for key_vpc in by_name["errors"]:
                if key_vpc["code"] == "not_found":
                    by_id = self.delete_network_acl_rule_by_id(acl, rule)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete network ACL rule by ID
    def delete_network_acl_rule_by_id(self, acl, id):
        try:
            # Check if network ACL exists
            acl_info = self.get_network_acl_by_name(acl)
            if "errors" in acl_info:
                return acl_info

            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/{}?version={}"
                    "&generation={}").format(acl_info["info"], id,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting network ACL rule with id {} for network"
                  "ACL {}. {}").format(id, acl, error)
            raise

    # Delete network ACL rule by name
    def delete_network_acl_rule_by_name(self, acl, name):
        try:
            # Check if network ACL and network ACL rule exist
            acl_info = self.get_network_acl_by_name(acl)
            rule_info = self.get_network_acl_rule_by_name(acl, name)
            if "errors" in acl_info:
                return acl_info
            elif "errors" in rule_info:
                return rule_info

            # Connect to api endpoint for network_acls
            path = ("/v1/network_acls/{}/rules/{}?version={}"
                    "&generation={}").format(acl_info["id"], rule_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting network ACL rule with name {} for network"
                  "ACL {}. {}").format(name, acl, error)
            raise
