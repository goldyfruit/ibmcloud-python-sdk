import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import subnet
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.utils.common import check_args
from ibmcloud_python_sdk import resource_group


class Vpn():

    def __init__(self):
        self.cfg = params()
        self.subnet = subnet.Subnet()
        self.rg = resource_group.Resource()

    def get_ike_policies(self):
        """
        Retrieve IKE policy list
        """
        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching IKE policies. {}".format(error))
            raise

    def get_ike_policy(self, policy):
        """
        Retrieve specific IKE policy
        :param policy: Policy name or ID
        """
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

    def get_ike_policy_by_id(self, id):
        """
        Retrieve specific IKE policy by ID
        :param id: IKE policy ID
        """
        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching IKE policy with ID {}. {}".format(id, error))
            raise

    def get_ike_policy_by_name(self, name):
        """
        Retrieve specific IKE policy by name
        :param name: IKE policy name
        """
        try:
            # Retrieve policies
            data = self.get_ike_policies()
            if "errors" in data:
                return data

            # Loop over policies until filter match
            for policy in data["ike_policies"]:
                if policy["name"] == name:
                    # Return data
                    return policy

            # Return error if no IKE policy is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching IKE policy with name {}. {}".format(
                name, error))
            raise

    def get_ike_policy_connections(self, policy):
        """
        Retrieve connections for an IKE policy
        :param policy: IKE policy name or ID
        """
        # Retrieve policy information
        policy_info = self.get_ike_policy(policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}/connections?version={}"
                    "&generation={}".format(policy_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection for IKE policy {}. {}".format(
                policy, error))
            raise

    def get_ipsec_policies(self):
        """
        Retrieve IPsec policy list
        """
        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching IPsec policies. {}".format(error))
            raise

    def get_ipsec_policy(self, policy):
        """
        Retrieve specific IPsec policy
        :param policy: Policy name or ID
        """
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

    def get_ipsec_policy_by_id(self, id):
        """
        Retrieve specific IPsec policy by ID
        :param id: IPsec policy ID
        """
        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching IPsec policy with ID {}. {}".format(
                id, error))
            raise

    def get_ipsec_policy_by_name(self, name):
        """
        Retrieve specific IPsec policy by name
        :param name: IPsec policy name
        """
        try:
            # Retrieve policies
            data = self.get_ipsec_policies()
            if "errors" in data:
                return data

            # Loop over policies until filter match
            for policy in data["ipsec_policies"]:
                if policy["name"] == name:
                    # Return data
                    return policy

            # Return error if no IPsec policy is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching IPsec policy with name {}. {}".format(
                name, error))
            raise

    def get_ipsec_policy_connections(self, policy):
        """
        Retrieve connections for an IPsec policy
        :param policy: IPsec policy name or ID
        """
        try:
            # Retrieve policy information by name to get the ID
            policy_info = self.get_ipsec_policy(policy)
            if "errors" in policy_info:
                return policy_info

            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}/connections?version={}"
                    "&generation={}".format(policy_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection for IPsec policy {}. {}".format(
                policy, error))
            raise

    def get_vpn_gateways(self):
        """
        Retrieve VPN gateway list
        """
        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPN gateways. {}".format(error))
            raise

    def get_vpn_gateway(self, gateway):
        """
        Retrieve specific VPN gateway
        :param gateway: VPN gateway name or ID
        """
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

    def get_vpn_gateway_by_id(self, id):
        """
        Retrieve specific VPN gateway by ID
        :param id: VPN gateway ID
        """
        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}?version={}&generation={}".format(
                id, self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching VPN gateway with ID {}. {}".format(
                id, error))
            raise

    def get_vpn_gateway_by_name(self, name):
        """
        Retrieve specific VPN gateway by name
        :param name: VPN gateway name
        """
        try:
            # Retrieve gateways
            data = self.get_vpn_gateways()
            if "errors" in data:
                return data

            # Loop over gateways until filter match
            for gateway in data["vpn_gateways"]:
                if gateway["name"] == name:
                    # Return data
                    return gateway

            # Return error if no VPN gateway is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching VPN gateway with name {}. {}".format(
                name, error))
            raise

    def get_vpn_gateway_connections(self, gateway):
        """
        Retrieve connections for a VPN gateway
        :param gateway: VPN gateway name or ID
        """
        # Retrieve gateway information by name to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections?version={}"
                    "&generation={}".format(gateway_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connections for VPN gateway {}. {}".format(
                gateway, error))
            raise

    def get_vpn_gateway_connection(self, gateway, connection):
        """
        Retrieve specific connection for a VPN gateway
        :param gateway: VPN gateway name or ID
        :param connection: Connection name or ID
        """
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

    def get_vpn_gateway_connection_by_id(self, gateway, id):
        """
        Retrieve specific connection for a VPN gateway by ID
        :param gateway: VPN gateway name or ID
        :param id: Connection ID
        """
        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}?version={}"
                    "&generation={}".format(gateway_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching connection with ID {} for VPN gateway with"
                  " ID {}. {}".format(gateway, id, error))
            raise

    def get_vpc_gateway_connection_by_name(self, gateway, name):
        """
        Retrieve specific connection for a VPN gateway by name
        :param gateway: VPN gateway name
        :param name: Connection name
        """
        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Retrieve gateway connections
            data = self.get_vpn_gateway_connections()
            if "errors" in data:
                return data

            # Loop over connections until filter match
            for connection in data["connections"]:
                if connection["name"] == name:
                    # Return data
                    return connection

            # Return error if no VPN gateway connection is found
            return resource_not_found()

        except Exception as error:
            print("Error fetching connection with name {} for VPN gateway"
                  " with name {}. {}".format(name, gateway, error))
            raise

    def get_vpn_gateway_local_cidrs(self, gateway, connection):
        """
        Retrieve local CIDR list on specific connection for a VPN gateway
        :param gateway: VPN gateway name
        :param connection: Connection name or ID
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching local CIDRs for connection {} in VPN gateway"
                  " {}. {}".format(connection, gateway, error))
            raise

    def check_vpn_gateway_local_cidr(self, gateway, connection, prefix_address,
                                     prefix_length):
        """
        Check if local CIDR exists on specific connection for a VPN gateway
        :param gateway: VPN gateway name
        :param connection: Connection name or ID
        :param prefix_address: The prefix address part of the CIDR
        :param prefix_length: The prefix length part of the CIDR
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       prefix_address,
                                                       prefix_length,
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching local CIDR {}/{} for connection {} in VPN"
                  " gateway {}. {}".format(prefix_address, prefix_length,
                                           connection, gateway, error))
            raise

    def get_vpn_gateway_peer_cidrs(self, gateway, connection):
        """
        Retrieve peer CIDR list on specific connection for a VPN gateway
        :param gateway: VPN gateway name
        :param connection: Connection name or ID
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching peer CIDRs for connection {} in VPN gateway"
                  " {}. {}".format(connection, gateway, error))
            raise

    # Check peer CIDR for specific connections on VPN gateway
    def check_vpn_gateway_peer_cidr(self, gateway, connection, prefix_address,
                                    prefix_length):
        """
        Check if local CIDR exists on specific connection for a VPN gateway
        :param gateway: VPN gateway name
        :param connection: Connection name or ID
        :param prefix_address: The prefix address part of the CIDR
        :param prefix_length: The prefix length part of the CIDR
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       prefix_address,
                                                       prefix_length,
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching peer CIDR {}/{} for connection {} in VPN"
                  " gateway {}. {}".format(prefix_address, prefix_length,
                                           connection, gateway, error))
            raise

    def create_ike_policy(self, **kwargs):
        """
        Create IKE policy
        :param name: Optional. The user-defined name for this IKE policy.
        :param resource_group: Optional. The resource group to use.
        :param authentication_algorithm: The authentication algorithm.
        :param dh_group: The Diffie-Hellman group.
        :param encryption_algorithm: The encryption algorithm.
        :param ike_version: The IKE protocol version.
        :param key_lifetime: The key lifetime in seconds.
        """
        args = ["authentication_algorithm", "dh_group",
                "encryption_algorithm", "ike_version"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
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
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating IKE policy. {}".format(error))
            raise

    def create_ipsec_policy(self, **kwargs):
        """
        Create IPsec policy
        :param name: Optional. The user-defined name for this IPsec policy.
        :param resource_group: Optional. The resource group to use.
        :param authentication_algorithm: The authentication algorithm.
        :param pfs: Perfect Forward Secrecy.
        :param encryption_algorithm: The encryption algorithm.
        :param key_lifetime: The key lifetime in seconds.
        """
        args = ["authentication_algorithm", "pfs",
                "encryption_algorithm"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
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
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating IPsec policy. {}".format(error))
            raise

    def create_gateway(self, **kwargs):
        """
        Create gateway
        :param name: Optional. The user-defined name for this gateway.
        :param resource_group: Optional. The resource group to use.
        :param subnet: Identifies a subnet by a unique property.
        """
        args = ["subnet"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'name': kwargs.get('name'),
            'resource_group': kwargs.get('resource_group'),
            'subnet': kwargs.get('subnet'),
        }

        # Retrieve subnet information to get the ID
        subnet_info = self.subnet.get_subnet(args["subnet"])
        if "errors" in subnet_info:
            return subnet_info

        # Construct payload
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "subnet":
                    payload["subnet"] = {"id": subnet_info["id"]}
                else:
                    payload[key] = value

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating gateway. {}".format(error))
            raise

    def create_connection(self, **kwargs):
        """
        Create connection
        :param gateway: The VPN gateway name or ID.
        :param name: Optional. The user-defined name for this connection.
        :param peer_address: The IP address of the peer VPN gateway.
        :param local_cidrs: Optional. A collection of local CIDRs.
        :param peer_cidrs: Optional. A collection of peer CIDRs.
        :param psk: Optional. The preshared key.
        :param admin_state_up: Optional. VPN connection shutdown if false.
        :param interval: Optional. Dead Peer Detection interval in seconds.
        :param timeout: Optional. Dead Peer Detection timeout in seconds.
        :param action: Optional. Dead Peer Detection actions.
        :param encryption_algorithm: The encryption algorithm.
        :param key_lifetime: The key lifetime in seconds.
        :param ike_policy: The absence of a policy indicates autonegotiation.
        :param ipsec_policy: The absence of a policy indicates autonegotiation.
        """
        args = ["gateway", "peer_address", "psk"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
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
                if key == "interval" or key == "timeout" or key == "action":
                    payload["dead_peer_detection"] = {
                        "internal": args["internal"],
                        "timeout": args["timeout"],
                        "action": args["action"]
                    }
                elif key == "ike_policy":
                    ike_info = self.get_ike_policy(args["ike_policy"])
                    if "errors" in ike_info:
                        return ike_info
                    payload["ike_policy"] = {"id": ike_info["id"]}
                elif key == "ipsec_policy":
                    ipsec_info = self.get_ipsec_policy(args["ipsec_policy"])
                    if "errors" in ipsec_info:
                        return ipsec_info
                    payload["ipsec_policy"] = {"id": ipsec_info["id"]}
                else:
                    payload[key] = value

        # Retrieve gateway information to get the ID
        # (mostly useful if a name is provided)
        gateway_info = self.get_vpn_gateway(args["gateway"])
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections?version={}"
                    "&generation={}".format(gateway_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating connection. {}".format(error))
            raise

    def add_local_cidr_connection(self, **kwargs):
        """
        Add local CIDR to a connection
        :param gateway: The VPN gateway name or ID.
        :param connection: The connection name or ID.
        :param prefix_address: The prefix address part of the CIDR.
        :param prefix_length: The prefix length part of the CIDR.
        """
        args = ["gateway", "connection", "prefix_address", "prefix_length"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'gateway': kwargs.get('gateway'),
            'connection': kwargs.get('resource_group'),
            'prefix_address': kwargs.get('prefix_address'),
            'prefix_length': kwargs.get('prefix_length'),
        }

        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(args["gateway"])
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(args["connection"])
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       args["prefix_address"],
                                                       args["prefix_length"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(), None)["data"]

        except Exception as error:
            print("Error addind local CIDR {}/{} to connection {} on VPN"
                  " gateway {}. {}".format(args["prefix_address"],
                                           args["prefix_length"],
                                           args["connection"],
                                           args["gateway"], error))
            raise

    def add_peer_cidr_connection(self, **kwargs):
        """
        Add peer CIDR to a connection
        :param gateway: The VPN gateway name or ID.
        :param connection: The connection name or ID.
        :param prefix_address: The prefix address part of the CIDR.
        :param prefix_length: The prefix length part of the CIDR.
        """
        args = ["gateway", "connection", "prefix_address", "prefix_length"]
        check_args(args, **kwargs)

        # Build dict of argument and assign default value when needed
        args = {
            'gateway': kwargs.get('gateway'),
            'connection': kwargs.get('resource_group'),
            'prefix_address': kwargs.get('prefix_address'),
            'prefix_length': kwargs.get('prefix_length'),
        }

        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(args["gateway"])
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(args["connection"])
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       args["prefix_address"],
                                                       args["prefix_length"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            # Return data
            return qw("iaas", "POST", path, headers(), None)["data"]

        except Exception as error:
            print("Error adding peer CIDR {}/{} to connection {} on VPN"
                  " gateway {}. {}").format(args["prefix_address"],
                                            args["prefix_length"],
                                            args["connection"],
                                            args["gateway"], error)
            raise

    def delete_ike_policy(self, policy):
        """
        Delete IKE policy
        :param policy: IKE policy name or ID
        """
        # Check if IKE policy exists
        policy_info = self.get_ike_policy(policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for ike_policies
            path = ("/v1/ike_policies/{}?version={}&generation={}".format(
                policy_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting IKE policy {}. {}".format(policy, error))
            raise

    def delete_ipsec_policy(self, policy):
        """
        Delete IPsec policy
        :param policy: IPsec policy name or ID
        """
        # Check if IPsec policy exists
        policy_info = self.get_ipsec_policy(policy)
        if "errors" in policy_info:
            return policy_info

        try:
            # Connect to api endpoint for ipsec_policies
            path = ("/v1/ipsec_policies/{}?version={}&generation={}".format(
                policy_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting IPsec policy {}. {}".format(policy, error))
            raise

    def delete_gateway(self, gateway):
        """
        Delete VPN gateway
        :param gateway: VPN gateway name or ID
        """
        # Check if gateway exists
        gateway_info = self.get_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}?version={}&generation={}".format(
                gateway_info["id"], self.cfg["version"],
                self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting VPN gateway {}. {}".format(gateway, error))
            raise

    def delete_connection(self, gateway, connection):
        """
        Delete connection
        :param gateway: VPN gateway name or ID
        :param connection: Connection name or ID
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}?version={}"
                    "&generation={}".format(gateway_info["id"],
                                            connection_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error deleting connection {} from VPN gateway {}."
                  " {}".format(gateway, connection, error))
            raise

    def remove_local_cidr(self, gateway, connection, prefix_address,
                          prefix_length):
        """
        Remove local CIDR from a connection
        :param gateway: VPN gateway name or ID
        :param connection: Connection name or ID
        :param prefix_address: The prefix address part of the CIDR.
        :param prefix_length: The prefix length part of the CIDR.
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/local_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       prefix_address,
                                                       prefix_length,
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error removing local CIDR {}/{} in connection {} from VPN"
                  " gateway {}. {}".format(prefix_address, prefix_length,
                                           connection,
                                           gateway, error))
            raise

    # Remove peer CIDR
    def remove_peer_cidr(self, gateway, connection, prefix_address,
                         prefix_length):
        """
        Remove peer CIDR from a connection
        :param gateway: VPN gateway name or ID
        :param connection: Connection name or ID
        :param prefix_address: The prefix address part of the CIDR.
        :param prefix_length: The prefix length part of the CIDR.
        """
        # Retrieve gateway information to get the ID
        gateway_info = self.get_vpn_gateway(gateway)
        if "errors" in gateway_info:
            return gateway_info

        # Retrieve connection information to get the ID
        connection_info = self.get_vpn_gateway_connection(connection)
        if "errors" in connection_info:
            return connection_info

        try:
            # Connect to api endpoint for vpn_gateways
            path = ("/v1/vpn_gateways/{}/connections/{}/peer_cidrs/{}/{}"
                    "?version={}&generation={}".format(gateway_info["id"],
                                                       connection_info["id"],
                                                       prefix_address,
                                                       prefix_length,
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            # Return data
            if data["response"].status != 204:
                return data["data"]

            # Return status
            return resource_deleted()

        except Exception as error:
            print("Error removing peer CIDR {}/{} in connection {} from VPN"
                  " gateway {}. {}".format(prefix_address, prefix_length,
                                           connection,
                                           gateway, error))
            raise
