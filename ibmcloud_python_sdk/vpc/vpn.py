import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import subnet


class Vpn():

    def __init__(self):
        self.cfg = params()
        self.subnet = subnet.Subnet()

    # Get all IKE policies
    def get_ike_policies(self):
        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching IKE policies. {error}")
            raise

    # Get specific IKE policy
    # This method is generic and should be used as prefered choice
    def get_ike_policy(self, policy):
        by_name = self.get_public_gateway_by_name(policy)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_public_gateway_by_id(policy)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific IKE policy by ID
    def get_ike_policy_by_id(self, id):
        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching IKE policy with ID {id}. {error}")
            raise

    # Get specific IKE policy by name
    def get_ike_policy_by_name(self, name):
        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve gateways data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over policies until filter match
            for policy in data["ike_policies"]:
                if policy["name"] == name:
                    # Return data
                    return policy

            # Return error if no IKE policy is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching IKE policy with name {name}. {error}")
            raise

    # Get connections for specific IKE policy
    def get_ike_policy_connections(self, policy):
        # Retrieve policy information by name to get the ID
        policy_info = self.get_ike_policy(policy)

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}/connections?version={}"
                    "&generation={}").format(policy_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection for IKE policy {}. {}").format(
                policy, error)
            raise

    # Get all IPsec policies
    def get_ipsec_policies(self):
        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching IPsec policies. {error}")
            raise

    # Get specific IPsec policy
    # This method is generic and should be used as prefered choice
    def get_ipsec_policy(self, policy):
        by_name = self.get_public_gateway_by_name(policy)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_public_gateway_by_id(policy)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific IPsec policy by ID
    def get_ipsec_policy_by_id(self, id):
        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching IPsec policy with ID {id}. {error}")
            raise

    # Get specific IPsec policy by name
    def get_ipsec_policy_by_name(self, name):
        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve gateways data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over policies until filter match
            for policy in data["ipsec_policies"]:
                if policy["name"] == name:
                    # Return data
                    return policy

            # Return error if no IPsec policy is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching IPsec policy with name {name}. {error}")
            raise

    # Get connections for specific IPsec policy
    def get_ipsec_policy_connections(self, policy):
        try:
            # Retrieve policy information by name to get the ID
            policy_info = self.get_ipsec_policy(policy)

            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}/connections?version={}"
                    "&generation={}").format(policy_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection for IPsec policy {}. {}").format(
                policy, error)
            raise

    # Get all VPN gateways
    def get_gateways(self):
        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching VPN gateways. {error}")
            raise

    # Get specific VPN gateway
    # This method is generic and should be used as prefered choice
    def get_gateway(self, gateway):
        by_name = self.get_gateway_by_name(gateway)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_gateway_by_id(gateway)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific VPN gateway by ID
    def get_gateway_by_id(self, id):
        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print(f"Error fetching VPN gateway with ID {id}. {error}")
            raise

    # Get specific VPN gateway by name
    def get_gateway_by_name(self, name):
        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Retrieve gateways data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over gateways until filter match
            for gateway in data["vpn_gateways"]:
                if gateway["name"] == name:
                    # Return data
                    return gateway

            # Return error if no VPN gateway is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print(f"Error fetching VPN gateway with name {name}. {error}")
            raise

    # Get connections for specific VPN gateway
    def get_connections(self, gateway):
        # Retrieve gateway information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections?version={}"
                    "&generation={}").format(gateway_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection for VPN gateway {}. {}").format(
                gateway, error)
            raise

    # Get specific VPN gateway connection
    # This method is generic and should be used as prefered choice
    def get_connection(self, gateway, connection):
        by_name = self.get_vpn_gateway_connection_by_name(gateway, connection)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_vpn_gateway_connection_by_id(gateway,
                                                                  connection)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    # Get specific VPN gateway connection by ID
    def get_connection_by_id(self, gateway, id):
        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}?version={}"
                    "&generation={}").format(gateway_info["id"], id,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection with ID {} for VPN gateway with"
                  " {}. {}").format(gateway, id, error)
            raise

    # Get specific VPN gateway connection by name
    def get_connection_by_name(self, gateway, name):
        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections?version={}"
                    "&generation={}").format(gateway_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Retrieve connections data
            data = qw("iaas", "GET", path, headers())["data"]

            # Loop over connections until filter match
            for connection in data["connections"]:
                if connection["name"] == name:
                    # Return data
                    return connection

            # Return error if no VPN gateway is found
            return {"errors": [{"code": "not_found"}]}

        except Exception as error:
            print("Error fetching connection with name {} for VPN gateway"
                  " with name {}. {}").format(name, gateway, error)
            raise

    # Get all local CIDRs for specific connections on VPN gateway
    def get_local_cidrs(self, gateway, connection):
        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        connection_info = self.get_vpn_gateway_connection(connection)

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching local CIDRs for connection {} in VPN gateway"
                  " {}. {}").format(connection, gateway, error)
            raise

    # Check local CIDR for specific connections on VPN gateway
    def check_local_cidr(self, gateway, connection, address, length):
        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        connection_info = self.get_vpn_gateway_connection(connection)

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        address, length,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching local CIDR {}/{} for connection {} in VPN"
                  " gateway {}. {}").format(address, length, connection,
                                            gateway, error)
            raise

    # Get all peer CIDRs for specific connections on VPN gateway
    def get_peer_cidrs(self, gateway, connection, address, length):
        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        connection_info = self.get_vpn_gateway_connection(connection)

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        address, length,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching peer CIDRs {}/{} for connection {} in VPN"
                  " gateway {}. {}").format(address, length, connection,
                                            gateway, error)
            raise

    # Check peer CIDR for specific connections on VPN gateway
    def check_peer_cidr(self, gateway, connection, address, length):
        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        connection_info = self.get_vpn_gateway_connection(connection)

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        address, length,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching peer CIDR {}/{} for connection {} in VPN"
                  " gateway {}. {}").format(address, length, connection,
                                            gateway, error)
            raise

    # Create IKE policy
    def create_ike_policy(self, **kwargs):
        # Required parameters
        required_args = set(["authentication_algorithm", "dh_group",
                             "encryption_algorithm", "ike_version"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'authentication_algorithm': kwargs.get('authentication_algorithm'),
            'dh_group': kwargs.get('dh_group'),
            'encryption_algorithm': kwargs.get('encryption_algorithm'),
            'ike_version': kwargs.get('ike_version'),
            'key_lifetime': kwargs.get('key_lifetime'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    payload["resource_group"] = {"id": args["resource_group"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating IKE policy. {error}")
            raise

    # Create IPsec policy
    def create_ipsec_policy(self, **kwargs):
        # Required parameters
        required_args = set(["authentication_algorithm", "pfs",
                             "encryption_algorithm"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'authentication_algorithm': kwargs.get('authentication_algorithm'),
            'pfs': kwargs.get('pfs'),
            'encryption_algorithm': kwargs.get('encryption_algorithm'),
            'key_lifetime': kwargs.get('key_lifetime'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    payload["resource_group"] = {"id": args["resource_group"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating IPsec policy. {error}")
            raise

    # Create gateway
    def create_gateway(self, **kwargs):
        # Required parameters
        required_args = set(["subnet"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'subnet': kwargs.get('subnet'),
        }

        # Retrieve subnet nformation by name to get the ID
        subnet_info = self.subnet.get_subnet(args["subnet"])

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    payload["resource_group"] = {"id": args["resource_group"]}
                elif key == "subnet":
                    payload["subnet"] = {"id": subnet_info["id"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating gateway. {error}")
            raise

    # Create connection
    def create_connection(self, **kwargs):
        # Required parameters
        required_args = set(["gateway", "peer_address", "psk"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'gateway': kwargs.get('gateway'),
            'name': kwargs.get('name'),
            'peer_address': kwargs.get('peer_address'),
            'local_cidrs': kwargs.get('local_cidrs'),
            'peer_cidrs': kwargs.get('peer_cidrs'),
            'psk': kwargs.get('psk'),
            'admin_state_up': kwargs.get('admin_state_up', True),
            'interval': kwargs.get('interval', 2),
            'timeout': kwargs.get('timeout', 10),
            'action': kwargs.get('action', "restart"),
            'encryption_algorithm': kwargs.get('encryption_algorithm'),
            'key_lifetime': kwargs.get('key_lifetime'),
            'ike_policy': kwargs.get('ike_policy'),
            'ipsec_policy': kwargs.get('ipsec_policy'),
        }

        # Construct payload
        payload = {}
        for key, value in args.items():
            if key != "gateway" and value is not None:
                if key == "resource_group":
                    payload["resource_group"] = {"id": args["resource_group"]}
                elif key == "interval" or key == "timeout" or key == "action":
                    payload["dead_peer_detection"] = {
                        "internal": args["internal"],
                        "timeout": args["timeout"],
                        "action": args["action"]
                    }
                elif key == "local_cidrs":
                    payload["local_cidrs"] = args["local_cidrs"]
                elif key == "peer_cidrs":
                    payload["peer_cidrs"] = args["peer_cidrs"]
                elif key == "ike_policy":
                    payload["ike_policy"] = {"id": args["ike_policy"]}
                elif key == "ipsec_policy":
                    payload["ipsec_policy"] = {"id": args["ipsec_policy"]}
                else:
                    payload[key] = value

        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway = self.get_vpn_gateway(args["gateway"])

        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/vpn_gateways/{}/connections?version={}"
                    "&generation={}").format(gateway["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print(f"Error creating connection. {error}")
            raise

    # Add local CIDR on resource connection
    def add_local_cidr_connection(self, **kwargs):
        # Required parameters
        required_args = set(["gateway", "connection", "address", "length"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'gateway': kwargs.get('gateway'),
            'connection': kwargs.get('resource_group'),
            'address': kwargs.get('address'),
            'length': kwargs.get('length'),
        }

        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(args["gateway"])
        connection_info = self.get_vpn_gateway_connection(args["connection"])

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        args["address"],
                                                        args["length"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(), None)["data"]

        except Exception as error:
            print("Error setting local CIDR {}/{} to connection {} on VPN"
                  " gateway {}. {}").format(args["address"], args["length"],
                                            args["connection"],
                                            args["gateway"], error)
            raise

    # Add peer CIDR on resource connection
    def add_peer_cidr_connection(self, **kwargs):
        # Required parameters
        required_args = set(["gateway", "connection", "address", "length"])
        if not required_args.issubset(set(kwargs.keys())):
            raise KeyError(
                f'Required param is missing. Required: {required_args}'
            )

        # Set default value is not required paramaters are not defined
        args = {
            'gateway': kwargs.get('gateway'),
            'connection': kwargs.get('resource_group'),
            'address': kwargs.get('address'),
            'length': kwargs.get('length'),
        }

        # Retrieve gateway and connection information by name to get the ID
        gateway_info = self.get_vpn_gateway(args["gateway"])
        connection_info = self.get_vpn_gateway_connection(args["connection"])

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        args["address"],
                                                        args["length"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            # Return data
            return qw("iaas", "POST", path, headers(), None)["data"]

        except Exception as error:
            print("Error setting peer CIDR {}/{} to connection {} on VPN"
                  " gateway {}. {}").format(args["address"], args["length"],
                                            args["connection"],
                                            args["gateway"], error)
            raise

    # Delete IKE policy
    def delete_ike_policy(self, policy):
        # Check if IKE policy exists
        policy_info = self.get_ike_policy(policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}?version={}&generation={}").format(
                policy_info["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting IKE policy {}. {}").format(id, error)
            raise

    # Delete IPsec policy
    def delete_ipsec_policy(self, policy):
        # Check if IPsec policy exists
        policy_info = self.get_ipsec_policy(policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}?version={}&generation={}").format(
                policy_info["id"], self.cfg["version"], self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting IPsec policy {}. {}").format(id, error)
            raise

    # Delete gateway
    def delete_gateway(self, gateway):
        # Check if gateway exists
        gateway_info = self.get_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}?version={}&generation={}").format(
                gateway_info["id"], self.cfg["version"],
                self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting gateway {}. {}").format(gateway, error)
            raise

    # Delete connection
    def delete_connection(self, gateway, connection):
        # Check if gateway and connection exists and retrieve information
        gateway_info = self.get_gateway(gateway)
        connection_info = self.get_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}?version={}"
                    "&generation={}").format(gateway_info["id"],
                                             connection_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting connection {} from VPN gateway {}."
                  " {}").format(gateway, connection, error)
            raise

    # Remove local CIDR
    def remove_local_cidr(self, gateway, connection, address, length):
        # Check if gateway and connection exists and retrieve information
        gateway_info = self.get_gateway(gateway)
        connection_info = self.get_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        address, length,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting local CIDR {}/{} in connection {} from VPN"
                  " gateway {}. {}").format(address, length, connection,
                                            gateway, error)
            raise

    # Remove peer CIDR
    def remove_peer_cidr(self, gateway, connection, address, length):
        # Check if gateway and connection exists and retrieve information
        gateway_info = self.get_gateway(gateway)
        connection_info = self.get_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}").format(gateway_info["id"],
                                                        connection_info["id"],
                                                        address, length,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return {"status": "deleted"}

        except Exception as error:
            print("Error deleting peer CIDR {}/{} in connection {} from VPN"
                  " gateway {}. {}").format(address, length, connection,
                                            gateway, error)
            raise
