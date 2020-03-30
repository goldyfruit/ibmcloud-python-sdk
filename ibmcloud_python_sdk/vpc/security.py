import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw


class Security():

    def __init__(self):
        self.cfg = params()

    # Get all security groups
    def get_security_groups(self):
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching security groups. {error}")
            raise

    # Get specific security group
    # This method is generic and should be used as prefered choice
    def get_security_group(self, sg):
        by_name = self.get_security_group_by_name(sg)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_security_group_by_id(sg)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific security group by ID
    def get_security_group_by_id(self, id):
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching security group with ID {id}. {error}")
            raise

    # Get specific security group by name
    def get_security_group_by_name(self, name):
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve security groups data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over security groups until filter match
            for sg in data['security_groups']:
                if sg["name"] == name:
                    # Return data
                    return sg

            # Return error if no security group is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching security group with name {name}. {error}")
            raise

    # Get network interfaces associated to security groups
    # This method is generic and should be used as prefered choice
    def get_security_group_interfaces(self, sg):
        by_name = self.get_security_group_by_name(sg)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_security_group_by_id(sg)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get network interfaces associated to security group by ID
    def get_security_group_interfaces_by_id(self, id):
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces associated to security"
                  " group with ID {}. {}").format(id, error)
            raise

    # Get network interfaces associated to security group by name
    def get_security_group_interfaces_by_name(self, name):
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg = self.get_security_group(name)
        if "errors" in sg:
            return sg

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces?version={}"
                    "&generation={}").format(sg["id"], self.cfg["version"],
                                             self.cfg["generation"])

            # Retrieve network interfaces data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over security groups until filter match
            for sg in data['security_groups']:
                if sg["name"] == name:
                    # Return data
                    return sg

            # Return error if no security group is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print("Error fetching network interfaces associated to security"
                  " group with name {}. {}").format(name, error)
            raise

    # Get security group's rules by ID
    def get_security_group_rules(self, security_group):
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(security_group)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules?version={}"
                    "&generation={}").format(sg_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rules for security group with"
                  " ID {}. {}").format(id, error)
            raise

    # Get specific security group's rule
    # This method is generic and should be used as prefered choice
    def get_security_group_rule(self, sg, rule):
        by_name = self.get_security_group_rule_by_name(sg, rule)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_security_group_rule_by_id(sg, rule)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific security group rule by ID
    def get_security_group_rule_by_id(self, sg, id):
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(sg)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules/{}?version={}"
                    "&generation={}").format(sg["info"], id,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching rule {} for security group with"
                  " ID {}. {}").format(id, sg["info"], error)
            raise

    # Get specific security group rules by name
    def get_security_group_rule_by_name(self, sg, name):
        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(sg)
        if "errors" in sg_info:
            return sg_info

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules/?version={}"
                    "&generation={}").format(sg_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Retrieve security groups data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over rules until filter match
            for rule in data['rules']:
                if rule["name"] == name:
                    # Return data
                    return rule

            # Return error if no security group is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print("Error fetching rule {} for security group with"
                  " name {}. {}").format(sg, name, error)
            raise

    # Add network interface to security group
    def add_interface_security_group(self, **kwargs):
        # Required parameters
        required_args = set(["security_group", "interface"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'interface': kwargs.get('interface'),
            'security_group': kwargs.get('security_group'),
        }

        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(args["security_group"])

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces/{}?version={}"
                    "&generation={}").format(sg_info["id"],
                                             args["interface"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "PUT", path, headers(), None)["data"]

        except Exception as error:
            print("Error adding network interface {} to security group"
                  " with ID {}. {}").format(args["interface"], sg_info["id"],
                                            error)
            raise

    # Create security group
    def create_security_group(self, **kwargs):
        # Required parameters
        required_args = set(["vpc"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

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
                    for sg_rules in args["rules"]:
                        tmp = {}
                        tmp["id"] = sg_rules
                        rs.append(tmp)
                    payload["rules"] = rs
            else:
                payload[key] = value

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating security group. {error}")
            raise

    # Create security group rule
    def create_security_group_rule(self, **kwargs):
        # Required parameters
        required_args = set(["sg", "direction"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
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

        # Construct payload
        payload = {}
        for key, value in args.items():
            # sg argument should not be in the payload
            if key != "sg" and value is not None:
                if key == "security_group":
                    payload["remote"] = {"id": args["security_group"]}
                elif key == "address":
                    payload["remote"] = {"address": args["address"]}
                elif key == "cidr_block":
                    payload["remote"] = {"cidr_block": args["cidr_block"]}
                else:
                    payload[key] = value

        # Retrieve security group information to get the ID
        # (mostly useful if a name is provided)
        sg_info = self.get_security_group(args["sg"])

        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules?version={}"
                    "&generation={}").format(sg_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating security group rule. {error}")
            raise

    # Delete security group
    # This method is generic and should be used as prefered choice
    def delete_security_group(self, security_group):
        by_name = self.delete_security_group_by_name(security_group)
        if "errors" in by_name:
            for key_vpc in by_name["errors"]:
                if key_vpc["code"] == "not_found":
                    by_id = self.delete_security_group_by_id(security_group)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Delete security group by ID
    def delete_security_group_by_id(self, id):
        try:
            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting security group with id {id}. {error}")
            raise

    # Delete security group by name
    def delete_security_group_by_name(self, name):
        try:
            # Check if security group exists
            sg_info = self.get_security_group_by_name(name)
            if "errors" in sg_info:
                return sg_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}?version={}&generation={}").format(
                sg_info["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print(f"Error deleting security group with name {name}. {error}")
            raise

    # Remove network interface from security group
    def remove_interface_security_group(self, security_group, interface):
        try:
            # Check if security group exists
            sg_info = self.get_security_group(security_group)
            if "errors" in sg_info:
                return sg_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/network_interfaces/{}?version={}"
                    "&generation={}").format(sg_info["id"], interface,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error removing network interface {} from security group"
                  " with name {}. {}").format(interface, security_group, error)
            raise

    # Delete security group rule
    def delete_security_group_rule(self, security_group, rule):
        try:
            # Check if security group exists
            sg_info = self.get_security_group(security_group)
            if "errors" in sg_info:
                return sg_info

            # Connect to api endpoint for security_groups
            path = ("/v1/security_groups/{}/rules/{}?version={}"
                    "&generation={}").format(sg_info["id"], rule,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting rule {} from security group {}. {}").format(
                rule, sg_info["id"], error
            )
            raise
