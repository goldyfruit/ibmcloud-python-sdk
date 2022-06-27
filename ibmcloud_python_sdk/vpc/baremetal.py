import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.vpc import image
from ibmcloud_python_sdk.vpc import subnet
from ibmcloud_python_sdk.vpc import security
from ibmcloud_python_sdk.vpc import floating_ip
from ibmcloud_python_sdk.vpc import volume
from ibmcloud_python_sdk.vpc import key as keyring
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk.resource import resource_group
from ibmcloud_python_sdk.utils.common import check_args


class Baremetal():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.image = image.Image()
        self.subnet = subnet.Subnet()
        self.security = security.Security()
        self.fip = floating_ip.Fip()
        self.volume = volume.Volume()
        self.keyring = keyring.Key()
        self.rg = resource_group.ResourceGroup()

    def get_servers(self):
        """Retrieve bare metal server list

        :return: List of bare metal server
        :rtype: list
        """
        try:
            path = ("/v1/bare_metal_servers?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching bare metal server. {}".format(error))
            raise

    def get_server(self, bare_metal_server):
        """Retrieve specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :return: Bare metal server information
        :rtype: dict
        """
        by_name = self.get_server_by_name(bare_metal_server)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_server_by_id(bare_metal_server)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_server_by_id(self, id):
        """Retrieve specific bare metal server by ID

        :param id: Bare metal server ID
        :type id: str
        :return: Bare metal server information
        :rtype: dict
        """
        try:
            path = ("/v1/bare_metal_servers/{}?version={}"
                    "&generation={}".format(
                        id, self.cfg["version"],
                        self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching bare metal server with ID {}. {}".format(id,
                  error))
            raise

    def get_server_by_name(self, name):
        """Retrieve specific bare metal server by name

        :param name: Bare metal server name
        :type name: str
        :return: Bare metal server information
        :rtype: dict
        """
        try:
            data = self.get_servers()
            if "errors" in data:
                return data

            for instance in data["bare_metal_servers"]:
                if instance["name"] == name:
                    return instance

            return resource_not_found()

        except Exception as error:
            print("Error fetching bare metal server with name {}. {}".format(
                name, error))
            raise

    def get_server_configuration(self, bare_metal_server):
        """Retrieve initial configuration for a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :return: Bare metal server configuration information
        :rtype: dict
        """
        by_name = self.get_server_configuration_by_name(
            bare_metal_server)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_server_configuration_by_id(
                        bare_metal_server)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_server_configuration_by_id(self, id):
        """Retrieve initial configuration for a specific instance by ID

        :param id: Bare metal server ID
        :type id: str
        :return: Bare metal server configuration information
        :rtype: dict
        """
        try:
            path = ("/v1/bare_metal_servers/{}/initialization?version={}"
                    "&generation={}".format(id, self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching configuration for bare metal server with ID"
                  " {}. {}".format(id, error))
            raise

    def get_server_configuration_by_name(self, name):
        """Retrieve initial configuration for a specific bare metal server by name

        :param name: Bare metal server name
        :type name: str
        :return: Bare metal server configuration information
        :rtype: dict
        """
        try:
            bare_metal_server_info = self.get_server(name)
            if "errors" in bare_metal_server_info:
                return bare_metal_server_info

            path = ("/v1/bare_metal_servers/{}/initialization?version={}"
                    "&generation={}".format(bare_metal_server_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching configuration for bare metal server"
                  "with name"
                  " {}. {}".format(name, error))
            raise

    def get_server_interfaces(self, bare_metal_server):
        """Retrieve network interfaces for a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :return: List of bare metal server's interfaces
        :rtype: list
        """
        by_name = self.get_server_interfaces_by_name(
            bare_metal_server)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_server_interfaces_by_id(
                        bare_metal_server)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_server_interfaces_by_id(self, id):
        """Retrieve network interfaces for a specific bare metal server by ID

        :param id: Bare metal ID
        :type id: str
        :return: List of bare metal server's interfaces
        :rtype: list
        """
        try:
            path = ("/v1/bare_metal_servers/{}/network_interfaces?version={}"
                    "&generation={}".format(id, self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces for bare metal server"
                  "with ID"
                  " {}. {}".format(id, error))
            raise

    def get_server_interfaces_by_name(self, name):
        """Retrieve network interfaces for a specific bare metal server by name

        :param name: Bare metal server name
        :type name: str
        :return: List of bare metal server's interfaces
        :rtype: list
        """
        bare_metal_server_info = self.get_server(name)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        try:
            path = ("/v1/bare_metal_servers/{}/network_interfaces?version={}"
                    "&generation={}".format(bare_metal_server_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces for bare metal server"
                  "with name"
                  " {}. {}".format(name, error))
            raise

    def get_server_interface(self, bare_metal_server, interface):
        """Retrieve specific network interface for a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param interface: Interface name or ID
        :type interface: str
        :return: Bare mental server's interface information
        :rtype: dict
        """
        by_name = self.get_server_interface_by_name(
            bare_metal_server, interface)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_server_interface_by_id(
                        bare_metal_server,
                        interface)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_server_interface_by_id(self, bare_metal_server, id):
        """Retrieve specific network interface for a specific bare metal server by ID

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param id: Interface ID
        :type id: str
        :return: Bare metal server's interface information
        :rtype: dict
        """
        bare_metal_server_info = self.get_server(bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        try:
            path = ("/v1/bare_metal_servers/{}"
                    "/network_interfaces/{}?version={}"
                    "&generation={}".format(bare_metal_server_info["id"], id,
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interface {} for bare metal server"
                  " {}. {}".format(bare_metal_server, id, error))
            raise

    def get_server_interface_by_name(self, bare_metal_server, name):
        """Retrieve specific network interface for a specific bare metal server by ID

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param name: Bare metal server name
        :type name: str
        :return: Bare metal server's interface information
        :rtype: dict
        """
        bare_metal_server_info = self.get_server(bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        try:
            data = self.get_server_interfaces(
                bare_metal_server_info["id"])
            if "errors" in data:
                return data

            for interface in data['network_interfaces']:
                if interface["name"] == name:
                    return interface

            return resource_not_found()

        except Exception as error:
            print("Error fetching network interface {} for instance"
                  " {}. {}".format(bare_metal_server, name, error))
            raise

    def get_server_interface_fips(self, bare_metal_server,
                                  interface):
        """Retrieve floating IPs attached to a network interface for a
        specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param bare_metal_server: Bare metal server name or ID
        :type interface: str
        :return: Floating IP list attached to a bare metal server
        :rtype: list
        """
        bare_metal_server_info = self.get_server(bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        interface_into = self.get_server_interface(
            bare_metal_server_info["id"],
            interface)
        if "errors" in interface_into:
            return interface_into

        try:
            path = ("/v1/bare_metal_servers/{}/network_interfaces/{}"
                    "/floating_ips"
                    "?version={}&generation={}".format(
                        bare_metal_server_info["id"],
                        interface_into["id"],
                        self.cfg["version"],
                        self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IPs attached to network interface"
                  " {} for instance {}. {}".format(
                      interface, bare_metal_server, error))
            raise

    def get_server_interface_fip(self, bare_metal_server, interface,
                                 floating):
        """Retrieve specific floating IP attached to a network interface for
        a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param interface: Interface name or ID
        :type interface: str
        :parem floating: Floating IP name, ID or address
        :type floating: str
        :return: Floating IP information
        :rtype: dict
        """
        bare_metal_server_info = self.get_server(bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        interface_into = self.get_server_interface(
            bare_metal_server_info["id"], interface)
        if "errors" in interface_into:
            return interface_into

        try:
            data = self.get_server_interface_fips(
                bare_metal_server_info["id"], interface_into["id"])
            if "errors" in data:
                return data

            fip_info = None
            for fip in data['floating_ips']:
                if (
                    fip["name"] == floating
                    or fip["id"] == floating
                    or fip["address"] == floating
                ):
                    fip_info = fip["id"]

            path = (
                "/v1/bare_metal_servers/{}/network_interfaces/{}"
                "/floating_ips/{}"
                "?version={}&generation={}".format(
                    bare_metal_server_info["id"],
                    interface_into["id"],
                    fip_info,
                    self.cfg["version"],
                    self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IP {} attached to network interface"
                  " {} for bare metal server {}. {}".format(
                      fip_info, interface, bare_metal_server, error))
            raise

    def get_server_disks(self, bare_metal_server):
        """Retrieve disks from a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :return: List of volume attachments
        :rtype: list
        """
        bare_metal_server_info = self.get_server(bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        try:
            path = ("/v1/bare_metal_servers/{}/disks"
                    "?version={}&generation={}".format(
                        bare_metal_server_info["id"],
                        self.cfg["version"],
                        self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print
            ("Error fetching disks on bare metal server {}. {}".format(
                bare_metal_server, error))
            raise

    def get_server_disk(self, bare_metal_server,
                        disk):
        """Retrieve a single disk from a specific bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param attachment: Volume attachment name or ID
        :type attachment: str
        :return: Volume attachment information
        :rtype: dict
        """
        bare_metal_server_info = self.get_server(
            bare_metal_server)
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        try:
            data = self.get_server_disks(
                bare_metal_server_info["id"])
            if "errors" in data:
                return data

            disk_info = None
            for hd in data['disks']:
                if hd["name"] == disk or hd["id"] == disk:
                    disk_info = hd["id"]

            path = ("/v1/bare_metal_servers/{}/disks/{}"
                    "?version={}&generation={}".format(
                        bare_metal_server_info["id"],
                        disk_info,
                        self.cfg["version"],
                        self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume {} attached to bare metal server"
                  " {}. {}".format(disk, bare_metal_server, error))
            raise

    def get_server_profiles(self):
        """Retrieve bare metal server profile list

        :return: List of bare metal server profiles:
        :rtype: list
        """
        try:
            path = ("/v1/bare_metal_server/profiles?version={}&generation={}".
                    format(self.cfg["version"], self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching bare metal server profiles. {}".format(
                error))
            raise

    def get_server_profile(self, profile):
        """Retrieve specific bare metal server profile

        :param profile: Bare metal server profile name or ID
        :type profile: str
        :return: Profile information
        :rtype: dict
        """
        try:
            path = ("/v1/bare_metal_server/profiles/{}?version={}"
                    "&generation={}".format(profile, self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching bare metal server profile {}. {}".format(
                profile, error))
            raise

    def create_bare_metal_server(self, **kwargs):
        """Create BMS

        :param name: The unique user-defined name for this bare metal server
            instance
        :type name: str, optional
        :param keys: The public SSH keys to install on the bare metal server
            instance
        :type keys: list, optional
        :param network_interfaces: Collection of additional network interfaces
            to create for the bare metal server instance
        :type network_interfaces: list of dicts, optional
        :param profile: The profile to use for this bare metal server instance
        :type profile: str
        :param resource_group: The resource group to use
        :type resource_group: str, optional
        :param user_data: User data to be made available when setting up the
            bare metal server instance
        :type user_data: str, optional
        :param image: The identity of the image to be used when provisioning
            the bare metal server instance
        :type image: str, optional
        :param primary_network_interface: Primary network interface
        :type primary_network_interface: dict
        :param vpc: The VPC the bare metal server instance is to be a part of
        :type vpc: str
        :param trusted_platform_module: .....
        :type trusted_platform_module: dict
          {
            "enabled": false,
            "mode": "tpm_2"
          }
        :param zone: The identity of the zone to provision the bare metal
            server instance in
        :type zone: str, optional
        """
        args = {
            'keys': kwargs.get('keys'),
            'name': kwargs.get('name'),
            'network_interfaces': kwargs.get('network_interfaces'),
            'profile': kwargs.get('profile'),
            'resource_group': kwargs.get('resource_group'),
            'user_data': kwargs.get('user_data'),
            'vpc': kwargs.get('vpc'),
            'image': kwargs.get('image'),
            'primary_network_interface': kwargs.get(
                'primary_network_interface'),
            'enable_secure_boot': kwargs.get('enable_secure_boot'),
            "trusted_platform_module": kwargs.get('trusted_platform_module'),
            'zone': kwargs.get('zone'),
        }
        base_payload = {}
        init_payload = {}
        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "profile":
                    base_payload["profile"] = {"name": args["profile"]}
                elif key == "keys":
                    kp = []
                    for key_pair in args["keys"]:
                        tmp_k = {}
                        key_info = self.keyring.get_key(key_pair)
                        if "errors" in key_info:
                            return key_info
                        tmp_k["id"] = key_info["id"]
                        kp.append(tmp_k)
                    init_payload["keys"] = kp
                elif key == "user_data":
                    init_payload["user_data"] = args["user_data"]
                elif key == "enable_secure_boot":
                    init_payload["enable_secure_boot"] = args[
                        "enable_secure_boot"]
                elif key == "trusted_platform_module":
                    init_payload["trusted_platform_module"] = args[
                        "trusted_platform_module"]
                elif key == "network_interfaces":
                    base_payload["network_interfaces"] = []
                    for interface in args["network_interfaces"]:
                        tmp_net_int = {}
                        for k_int, v_int in interface.items():
                            if k_int == "name" and v_int != "":
                                tmp_net_int["name"] = v_int
                            if k_int == "interface_type" and v_int != "":
                                tmp_net_int["interface_type"] = v_int
                            if k_int == "vlan" and v_int != "":
                                tmp_net_int["vlan"] = v_int
                            if k_int == "allow_interface_to_float" and v_int != "":
                                tmp_net_int["allow_interface_to_float"] = v_int
                            if k_int == "enable_infrastructure_nat" and v_int != "":
                                tmp_net_int["enable_infrastructure_nat"] = v_int
                            if k_int == "allow_ip_spoofing" and v_int != "":
                                tmp_net_int["allow_ip_spoofing"] = v_int
                            if k_int == "subnet" and v_int != "":
                                subnet_info = self.subnet.get_subnet(v_int)
                                tmp_net_int["subnet"] = {
                                    "id": subnet_info["id"]}
                            if k_int == "security_groups":
                                sg_array = []
                                for security_group in v_int:
                                    if security_group != "":
                                        sg_info = self.security.get_security_group(
                                            security_group)
                                        sg_array.append({"id": sg_info["id"]})
                                tmp_net_int["security_groups"] = sg_array
                            # network_interfaces.append(tmp_net_int)
                        base_payload["network_interfaces"].append(tmp_net_int)
                elif key == "primary_network_interface":
                    tmp_pni = {}
                    for k_pni, v_pni in args["primary_network_interface"].items():
                        if k_pni == "name" and v_pni != "":
                            tmp_pni["name"] = v_pni
                        if k_pni == "interface_type" and v_pni != "":
                            tmp_pni["interface_type"] = v_pni or "pci"
                        if k_pni == "vlan" and v_pni != "":
                            tmp_pni["vlan"] = v_pni
                        if k_pni == "allow_interface_to_float" and v_pni != "":
                            tmp_pni["allow_interface_to_float"] = v_pni
                        if k_pni == "enable_infrastructure_nat" and v_pni != "":
                            tmp_pni["enable_infrastructure_nat"] = v_pni
                        if k_pni == "allow_ip_spoofing" and v_pni != "":
                            tmp_pni["allow_ip_spoofing"] = v_pni
                        if k_pni == "subnet" and v_pni != "":
                            subnet_info = self.subnet.get_subnet(
                                v_pni)
                            tmp_pni["subnet"] = {"id": subnet_info["id"]}
                        if k_pni == "security_groups":
                            sg_array = []
                            for security_group in v_pni:
                                if security_group != "":
                                    sg_info = self.security.get_security_group(
                                        security_group)
                                    sg_array.append({"id": sg_info["id"]})
                            tmp_pni["security_groups"] = sg_array
                    base_payload["primary_network_interface"] = tmp_pni
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    base_payload["resource_group"] = {"id": rg_info["id"]}
                    vpc_info = self.vpc.get_vpc(args["vpc"])
                    if "errors" in vpc_info:
                        return vpc_info
                    base_payload["vpc"] = {"id": vpc_info["id"]}
                elif key == "image":
                    image_info = self.image.get_image(args["image"])
                    if "errors" in image_info:
                        return image_info
                    init_payload["image"] = {"id": image_info["id"]}
                elif key == "image":
                    image_info = self.image.get_image(args["image"])
                    if "errors" in image_info:
                        return image_info
                    payload["image"] = {"id": image_info["id"]}
                elif key == "zone":
                    base_payload["zone"] = {"name": args["zone"]}
                elif key == "name":
                    base_payload["name"] = args["name"]
                else:
                    payload[key] = value

        payload = base_payload
        payload["initialization"] = init_payload

        try:
            path = ("/v1/bare_metal_servers?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating bare metal server. {}".format(error))
            raise

    def create_bare_metal_server_action(self, **kwargs):
        """Create bare metal server action

        :param bare_metal_server: The bare metal server name or ID
        :type bare_metal_server: str
        :param action: The action to execute (start, restart, stop)
        :type type: str
        :param type: If hard, the action will be forced immediately,
            and all queued actions deleted. Ignored for the start action
            (hard or soft)
        :type force: str
        """
        args = ["bare_metal_server", "action"]
        check_args(args, **kwargs)

        args = {
            'bare_metal_server': kwargs.get('bare_metal_server'),
            'type': kwargs.get('type'),
            'action': kwargs.get('action'),
        }

        bare_metal_server_info = self.get_server(
            args["bare_metal_server"])
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        payload = {}
        for key, value in args.items():
            if key == "type" and value is not None:
                payload[key] = value

        print(payload)

        try:
            path = ("/v1/bare_metal_servers/{}/{}?version={}"
                    "&generation={}".format(bare_metal_server_info["id"],
                                            args["action"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating bare metal server action. {}".format(error))
            raise

    def create_bare_metal_server_interface(self, **kwargs):
        """Create bare metal server interface

        :param bare_metal_server: The bare metal server name or ID
        :type bare_metal_server: str
        :param subnet: The associated subnet name or ID
        :type subnet: str
        :param primary_ipv4_address: The primary IPv4 address
        :type primary_ipv4_address: str, optional
        :param security_groups: Collection of security groups
        :type security_groups: str, optional
        """
        args = ["bare_metal_server", "subnet"]
        check_args(args, **kwargs)

        args = {
            'bare_metal_server': kwargs.get('bare_metal_server'),
            'subnet': kwargs.get('forsubnetce'),
            'primary_ipv4_address': kwargs.get('primary_ipv4_address'),
            'security_groups': kwargs.get('security_groups'),
        }

        bare_metal_server_info = self.get_server(
            args["bare_metal_server"])
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        subnet_info = self.subnet.get_subnet(args["subnet"])
        if "errors" in subnet_info:
            return subnet_info

        payload = {}
        for key, value in args.items():
            if key != "bare_metal_server" and value is not None:
                if key == "security_groups":
                    sg = []
                    for key_sg in args["security_groups"]:
                        tmp_sg = {}
                        tmp_sg["id"] = key_sg
                        sg.append(tmp_sg)
                    payload["security_groups"] = sg
                elif key == "subnet":
                    payload["subnet"] = {"id": subnet_info["id"]}
                else:
                    payload[key] = value

        try:
            path = ("/v1/bare_metal_servers/{}/network_interfaces?version={}"
                    "&generation={}".format(bare_metal_server_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating bare metal server interface. {}".format(
                error))
            raise

    def associate_floating_ip(self, **kwargs):
        """Associate floating IP with a network interface on an bare metal server

        :param server: Bare metal server name or ID
        :type server: str
        :param interface: The network interface name or ID¨
        :type interface: str
        :param fip: The floting IP name, ID or address
        :type fip: str
        """
        args = ["server", "interface", "fip"]
        check_args(args, **kwargs)

        args = {
            'server': kwargs.get('server'),
            'interface': kwargs.get('interface'),
            'fip': kwargs.get('fip'),
        }

        server_info = self.get_server(
            args["server"])
        if "errors" in server_info:
            return server_info

        interface_info = self.get_server_interface(
            server_info["id"],
            args["interface"])
        if "errors" in interface_info:
            return interface_info

        fip_info = self.fip.get_floating_ip(args["fip"])
        if "errors" in fip_info:
            return fip_info

        try:
            path = ("/v1/bare_metal_servers/{}/network_interfaces/{}"
                    "/floating_ips/{}"
                    "?version={}&generation={}".format(
                        server_info["id"],
                        interface_info["id"],
                        fip_info["id"],
                        self.cfg["version"],
                        self.cfg["generation"]))

            return qw("iaas", "PUT", path, headers(), None)["data"]

        except Exception as error:
            print("Error associating floating IP {} on network interface {}"
                  " for bare metal server {}. {}".format(
                      fip_info["id"],
                      interface_info["id"],
                      server_info["id"], error))
            raise

    def attach_volume(self, **kwargs):
        """Attach a volume to an bare metal server

        :param bare_metal_server: The bare metal server name or ID
        :type bare_metal_server: str
        :param volume: The identity of the volume to attach to the bare
            metal server
        :type volume: str
        :param delete_volume_on_bare_metal_server_delete: If set to true,
            when deleting the bare_metal_server the volume will also
            be deleted
        :type delete_volume_on_bare_metal_server_delete: bool, optional
        :param name: The user-defined name for this volume attachment
        :type name: str
        """
        args = ["bare_metal_server", "volume"]
        check_args(args, **kwargs)

        args = {
            'bare_metal_server': kwargs.get('bare_metal_server'),
            'volume': kwargs.get('volume'),
            'delete_volume_on_bare_metal_server_delete': kwargs.get(
                'delete_volume_on_bare_metal_server_delete'),
            'name': kwargs.get('name'),
        }

        bare_metal_server_info = self.get_server(
            args["bare_metal_server"])
        if "errors" in bare_metal_server_info:
            return bare_metal_server_info

        volume_info = self.volume.get_volume(args["volume"])
        if "errors" in volume_info:
            return volume_info

        payload = {}
        for key, value in args.items():
            if key != "bare_metal_server" and value is not None:
                if key == "volume":
                    payload["volume"] = {"id": volume_info["id"]}
                else:
                    payload[key] = value

        try:
            path = ("/v1/bare_metal_servers/{}/volume_attachments?version={}"
                    "&generation={}".format(bare_metal_server_info["id"],
                                            self.cfg["version"],
                                            self.cfg["generation"]))

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating volume attachment. {}".format(error))
            raise

    def delete_bare_metal_server(self, bare_metal_server):
        """Delete bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :return: Delete status
        :rtype: dict
        """
        try:
            bare_metal_server_info = self.get_server(
                bare_metal_server)
            if "errors" in bare_metal_server_info:
                return bare_metal_server_info

            path = (
                "/v1/bare_metal_servers/{}?version={}&generation={}".format(
                    bare_metal_server_info["id"], self.cfg["version"],
                    self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error deleting bare metal server {}. {}".format(
                bare_metal_server, error))
            raise

    def delete_bare_metal_server_interface(self, bare_metal_server, interface):
        """Delete interface from bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param interface: Interface name or ID
        :type interface: str
        :return: Delete status
        :rtype: dict
        """
        try:
            bare_metal_server_info = self.get_server(
                bare_metal_server)
            if "errors" in bare_metal_server_info:
                return bare_metal_server_info

            interface_info = self.get_server_interface(interface)
            if "errors" in interface_info:
                return interface_info

            path = (
                "/v1/bare_metal_servers/{}/network_interfaces/{}?version={}"
                "&generation={}".format(bare_metal_server_info["id"],
                                        interface_info["id"],
                                        self.cfg["version"],
                                        self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error deleting bare metal server {}. {}".format(
                bare_metal_server, error))
            raise

    def disassociate_floating_ip(self, bare_metal_server, interface, fip):
        """Disassociate floating IP from a network interface on an bare metal server

        :param bare_metal_server: Bare metal server name or ID
        :type bare_metal_server: str
        :param interface: Interface name or ID
        :type interface: str
        :parem fip: Floating IP name, ID or address
        :type fip: str
        """
        try:
            bare_metal_server_info = self.get_server(
                bare_metal_server)
            if "errors" in bare_metal_server_info:
                return bare_metal_server_info

            interface_info = self.get_server_interface(
                bare_metal_server, interface)
            if "errors" in interface_info:
                return interface_info

            fip_info = self.fip.get_floating_ip(fip)
            if "errors" in fip_info:
                return fip_info

            path = (
                "/v1/bare_metal_servers/{}/network_interfaces/{}"
                "/floating_ips/{}"
                "?version={}&generation={}".format(
                    bare_metal_server_info["id"],
                    interface_info["id"],
                    fip_info["id"],
                    self.cfg["version"],
                    self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error disassociating floating IP {} from network interface"
                  " {} on bare metal server {}. {}".format(
                      fip, interface, bare_metal_server,
                      error))
            raise
