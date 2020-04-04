import json
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.auth import get_headers as headers
from ibmcloud_python_sdk.utils.common import query_wrapper as qw
from ibmcloud_python_sdk.vpc import vpc
from ibmcloud_python_sdk.vpc import image
from ibmcloud_python_sdk.vpc import subnet
from ibmcloud_python_sdk.vpc import floating_ip
from ibmcloud_python_sdk.vpc import volume
from ibmcloud_python_sdk.utils.common import resource_not_found
from ibmcloud_python_sdk.utils.common import resource_deleted
from ibmcloud_python_sdk import resource_group
from ibmcloud_python_sdk.utils.common import check_args


class Instance():

    def __init__(self):
        self.cfg = params()
        self.vpc = vpc.Vpc()
        self.image = image.Image()
        self.subnet = subnet.Subnet()
        self.fip = floating_ip.Fip()
        self.volume = volume.Volume()
        self.rg = resource_group.Resource()

    def get_instances(self):
        """
        Retrieve instances list
        """
        try:
            path = ("/v1/instances?version={}&generation={}".format(
                self.cfg["version"], self.cfg["generation"]))

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching instances. {}").format(error)
            raise

    def get_instance(self, instance):
        """
        Retrieve specific instance
        :param instance: Instance name or ID
        """
        by_name = self.get_instance_by_name(instance)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_by_id(instance)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_instance_by_id(self, id):
        """
        Retrieve specific instance by ID
        :param id: Instance ID
        """
        try:
            path = ("/v1/instances/{}?version={}&generation={}").format(
                id, self.cfg["version"], self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching instance with ID {}. {}").format(id, error)
            raise

    def get_instance_by_name(self, name):
        """
        Retrieve specific instance by name
        :param name: Instance name
        """
        try:
            data = self.get_instances()
            if "errors" in data:
                return data

            for instance in data["instances"]:
                if instance["name"] == name:
                    return instance

            return resource_not_found()

        except Exception as error:
            print("Error fetching instance with name {}. {}").format(
                name, error)
            raise

    def get_instance_configuration(self, instance):
        """
        Retrieve initial configuration for a specific instance
        :param instance: Instance name or ID
        """
        by_name = self.get_instance_configuration_by_name(instance)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_configuration_by_id(instance)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_instance_configuration_by_id(self, id):
        """
        Retrieve initial configuration for a specific instance by ID
        :param id: Instance ID
        """
        try:
            path = ("/v1/instances/{}/initialization?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching configuration for instance with ID"
                  " {}. {}").format(id, error)
            raise

    def get_instance_configuration_by_name(self, name):
        """
        Retrieve initial configuration for a specific instance by name
        :param name: Instance name
        """
        try:
            instance_info = self.get_instance(name)
            if "errors" in instance_info:
                return instance_info

            path = ("/v1/instances/{}/initialization?version={}"
                    "&generation={}").format(instance_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching configuration for instance with name"
                  " {}. {}").format(name, error)
            raise

    def get_instance_interfaces(self, instance):
        """
        Retrieve network interfaces for a specific instance
        :param instance: Instance name or ID
        """
        by_name = self.get_instance_interfaces_by_name(instance)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_interfaces_by_id(instance)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_instance_interfaces_by_id(self, id):
        """
        Retrieve network interfaces for a specific instance by ID
        :param id: Instance ID
        """
        try:
            path = ("/v1/instances/{}/network_interfaces?version={}"
                    "&generation={}").format(id, self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces for instance with ID"
                  " {}. {}").format(id, error)
            raise

    def get_instance_interfaces_by_name(self, name):
        """
        Retrieve network interfaces for a specific instance by name
        :param name: Instance name
        """
        instance_info = self.get_instance(name)
        if "errors" in instance_info:
            return instance_info

        try:
            path = ("/v1/instances/{}/network_interfaces?version={}"
                    "&generation={}").format(instance_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interfaces for instance with name"
                  " {}. {}").format(name, error)
            raise

    def get_instance_interface(self, instance, interface):
        """
        Retrieve specific network interface for a specific instance
        :param instance: Instance name or ID
        :param interface: Interface name or ID
        """
        by_name = self.get_instance_interface_by_name(instance, interface)
        if "errors" in by_name:
            for key_name in by_name["errors"]:
                if key_name["code"] == "not_found":
                    by_id = self.get_instance_interface_by_id(instance,
                                                              interface)
                    if "errors" in by_id:
                        return by_id
                    return by_id
                else:
                    return by_name
        else:
            return by_name

    def get_instance_interface_by_id(self, instance, id):
        """
        Retrieve specific network interface for a specific instance by ID
        :param instance: Instance name or ID
        :param id: Interface ID
        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        try:
            path = ("/v1/instances/{}/network_interfaces/{}?version={}"
                    "&generation={}").format(instance_info["id"], id,
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching network interface {} for instance"
                  " {}. {}").format(instance, id, error)
            raise

    def get_instance_interface_by_name(self, instance, name):
        """
        Retrieve specific network interface for a specific instance by ID
        :param instance: Instance name or ID
        :param name: Interface name
        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        try:
            data = self.get_instance_interfaces(instance_info["id"])
            if "errors" in data:
                return data

            for interface in data['network_interfaces']:
                if interface["name"] == name:
                    return interface

            return resource_not_found()

        except Exception as error:
            print("Error fetching network interface {} for instance"
                  " {}. {}").format(instance, name, error)
            raise

    def get_instance_interface_fips(self, instance, interface):
        """
        Retrieve floating IPs attached to a network interface for a specific
        instance
        :param instance: Instance name or ID
        :param interface: Interface name or ID
        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        interface_into = self.get_instance_interface(instance_info["id"],
                                                     interface)
        if "errors" in interface_into:
            return interface_into

        try:
            path = ("/v1/instances/{}/network_interfaces/{}/floating_ips"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        interface_into["id"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IPs attached to network interface"
                  " {} for instance {}. {}").format(interface, instance, error)
            raise

    def get_instance_interface_fip(self, instance, interface, floating):
        """
        Retrieve floating IPs attached to a network interface for a specific
        instance
        :param instance: Instance name or ID
        :param interface: Interface name or ID
        :parem fip: Floating IP name,ID or address
        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        interface_into = self.get_instance_interface(
            instance_info["id"], interface)
        if "errors" in interface_into:
            return interface_into

        try:
            data = self.get_instance_interface_fips(
                instance_info["id"], interface_into["id"])
            if "errors" in data:
                return data

            for fip in data['floating_ips']:
                fn = fip["name"]
                fi = fip["id"]
                fa = fip["address"]
                if fn == floating or fi == floating or fa == floating:
                    fip_info = fip["id"]

            path = ("/v1/instances/{}/network_interfaces/{}/floating_ips/{}"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        interface_into["id"],
                                                        fip_info,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching floating IP {} attached to network interface"
                  " {} for instance {}. {}").format(fip_info, interface,
                                                    instance, error)
            raise

    def get_instance_volume_attachments(self, instance):
        """
        Retrieve volume attachments to a specific instance
        :param instance: Instance name or ID
        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        try:
            path = ("/v1/instances/{}/volume_attachments"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volumes attached to instance {}. {}").format(
                instance, error)
            raise

    def get_instance_volume_attachment(self, instance, attachment):
        """
        Retrieve specific volume attached to a specific instance
        :param instance: Instance name or ID
        :param attachment: Volume attachment name or ID

        """
        instance_info = self.get_instance(instance)
        if "errors" in instance_info:
            return instance_info

        try:
            data = self.get_instance_volume_attachments(instance_info["id"])
            if "errors" in data:
                return data

            for vol in data['volume_attachments']:
                if vol["name"] == attachment or vol["id"] == attachment:
                    volume_info = vol["id"]

            path = ("/v1/instances/{}/volume_attachments/{}"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        volume_info,
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching volume {} attached to instance"
                  " {}. {}").format(attachment, instance, error)
            raise

    def get_instance_profiles(self):
        """
        Retrieve instance profile list
        """
        try:
            path = ("/v1/instance/profiles?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching instance profiles. {}").format(error)
            raise

    def get_instance_profile(self, profile):
        """
        Retrieve specific instance profile
        :param profile: Instance profile name or ID
        """
        try:
            path = ("/v1/instance/profiles/{}?version={}"
                    "&generation={}").format(profile, self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "GET", path, headers())["data"]

        except Exception as error:
            print("Error fetching instance profile {}. {}").format(
                profile, error)
            raise

    def create_instance(self, **kwargs):
        """
        Create instance
        :param name: Optional. The unique user-defined name for this virtual
        server instance.

        :param keys: Optional. The public SSH keys to install on the virtual
        server instance.

        :param network_interfaces: Optional. Collection of additional network
        interfaces to create for the virtual server instance.

        :param placement_target: Optional. The placement for the virtual server
        instance.

        :param profile: Optional. The profile to use for this virtual server
        instance.

        :param resource_group: Optional. The resource group to use.

        :param user_data: Optional. User data to be made available when setting
        up the virtual server instance.

        :param volume_attachments: Optional. Collection of volume attachments.

        :param boot_volume_attachment: Optional. The boot volume attachment for
        the virtual server instance.

        :param source_template: Optional. The unique identifier for this
        instance template.

        :param image: Optional. The identity of the image to be used when
        provisioning the virtual server instance.

        :param primary_network_interface: Optional. Primary network interface.

        :param vpc: Optional. The VPC the virtual server instance is to be a
        part of.

        :param zone: Optional. The identity of the zone to provision the
        virtual server instance in.
        """
        args = {
            'keys': kwargs.get('keys'),
            'name': kwargs.get('name'),
            'network_interfaces': kwargs.get('network_interfaces'),
            'placement_target': kwargs.get('placement_target'),
            'profile': kwargs.get('profile'),
            'resource_group': kwargs.get('resource_group'),
            'user_data': kwargs.get('user_data'),
            'volume_attachments': kwargs.get('volume_attachments'),
            'vpc': kwargs.get('vpc'),
            'boot_volume_attachment': kwargs.get('boot_volume_attachment'),
            'source_template': kwargs.get('source_template'),
            'image': kwargs.get('image'),
            'primary_network_interface': kwargs.get(
                'primary_network_interface'),
            'zone': kwargs.get('zone'),
        }

        payload = {}
        for key, value in args.items():
            if value is not None:
                if key == "profile":
                    payload["profile"] = {"name": args["profile"]}
                elif key == "keys":
                    kp = []
                    for key_pair in args["keys"]:
                        tmp_k = {}
                        tmp_k["id"] = key_pair
                        kp.append(tmp_k)
                    payload["keys"] = kp
                elif key == "network_interfaces":
                    nics = []
                    for interface in args["network_interfaces"]:
                        tmp_n = {}
                        for nic_k, nic_v in interface.items():
                            if nic_v is not None:
                                if nic_k == "security_groups":
                                    sg = []
                                    for nic_sg in interface["security_groups"]:
                                        tmp_sg = {}
                                        tmp_sg["id"] = nic_sg
                                        sg.append(tmp_sg)
                                    tmp_n["security_groups"] = sg
                                elif nic_k == "ips":
                                    ip = []
                                    for nic_ip in interface["ips"]:
                                        tmp_ip = {}
                                        tmp_ip["id"] = nic_ip
                                        ip.append(tmp_ip)
                                    tmp_n["ips"] = ip
                                elif nic_k == "primary_ip":
                                    tmp_n["primary_ip"] = {
                                        "id": interface["primary_ip"]}
                                else:
                                    tmp_n[nic_k] = nic_v
                        nics.append(tmp_n)
                        payload["network_interfaces"] = nics
                elif key == "volume_attachments":
                    volumes = []
                    for vol_att in args["volume_attachments"]:
                        tmp_v = {}
                        for vol_k, vol_v in vol_att.items():
                            if vol_v is not None:
                                if vol_k == "volume":
                                    tmp_v["volume"] = {"id": vol_att["volume"]}
                                else:
                                    tmp_v[vol_k] = vol_v
                        volumes.append(tmp_v)
                        payload["volume_attachments"] = volumes
                elif key == "boot_volume_attachment":
                    tmp_b = {}
                    bva = args["boot_volume_attachment"]
                    for boot_k, boot_v in bva.items():
                        if boot_k == "profile":
                            tmp_b["profile"] = {"name": boot_v}
                        elif boot_k == "resource_group":
                            tmp_b["resource_group"] = {"id": boot_v}
                        elif boot_k == "encryption_key":
                            tmp_b["encryption_key"] = {"crn": boot_v}
                        else:
                            tmp_b[boot_k] = boot_v
                    payload["boot_volume_attachments"] = tmp_b
                elif key == "primary_network_interface":
                    tmp_p = {}
                    pni = args["primary_network_interface"]
                    for pni_k, pni_v in pni.items():
                        if pni_v is not None:
                            if pni_k == "security_groups":
                                sg = []
                                for pni_sg in pni["security_groups"]:
                                    tmp_sg = {}
                                    tmp_sg["id"] = pni_sg
                                    sg.append(tmp_sg)
                                tmp_p["security_groups"] = sg
                            elif pni_k == "ips":
                                ip = []
                                for pni_ip in pni["ips"]:
                                    tmp_ip = {}
                                    tmp_ip["id"] = pni_ip
                                    ip.append(tmp_ip)
                                tmp_p["ips"] = ip
                            elif nic_k == "primary_ip":
                                tmp_n["primary_ip"] = {
                                    "id": interface["primary_ip"]}
                            else:
                                tmp_p[pni_k] = pni_v
                    payload["primary_network_interface"] = tmp_p
                elif key == "resource_group":
                    rg_info = self.rg.get_resource_group(
                        args["resource_group"])
                    if "errors" in rg_info:
                        return rg_info
                    payload["resource_group"] = {"id": rg_info["id"]}
                elif key == "vpc":
                    vpc_info = self.vpc.get_vpc(args["vpc"])
                    if "errors" in vpc_info:
                        return vpc_info
                    payload["vpc"] = {"id": vpc_info["id"]}
                elif key == "image":
                    image_info = self.image.get_image(args["image"])
                    if "errors" in image_info:
                        return image_info
                    payload["image"] = {"id": image_info["id"]}
                elif key == "image":
                    image_info = self.image.get_image(args["image"])
                    if "errors" in image_info:
                        return image_info
                    payload["image"] = {"id": image_info["id"]}
                elif key == "source_template":
                    payload["source_template"] = {
                        "id": args["source_template"]}
                else:
                    payload[key] = value

        try:
            path = ("/v1/instances?version={}&generation={}").format(
                self.cfg["version"], self.cfg["generation"])

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating instance. {}").format(error)
            raise

    def create_instance_action(self, **kwargs):
        """
        Create instance action
        :param instance: The instance name or ID.

        :param type: The type of action.

        :param force: Optional. If set to true, the action will be forced
        immediately, and all queued actions deleted. Ignored for the start
        action.
        """
        args = ["instance", "type"]
        check_args(args, **kwargs)

        args = {
            'instance': kwargs.get('instance'),
            'force': kwargs.get('force'),
            'type': kwargs.get('type'),
        }

        instance_info = self.get_instance(args["instance"])
        if "errors" in instance_info:
            return instance_info

        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                payload[key] = value

        try:
            path = ("/v1/instances/{}/actions?version={}"
                    "&generation={}").format(instance_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating instance action. {}").format(error)
            raise

    def create_instance_interface(self, **kwargs):
        """
        Create instance interface
        :param instance: The instance name or ID.

        :param subnet: The associated subnet name or ID

        :param primary_ipv4_address: Optional. The primary IPv4 address.

        :param security_groups: Optional. Collection of security groups.
        """
        args = ["instance", "subnet"]
        check_args(args, **kwargs)

        args = {
            'instance': kwargs.get('instance'),
            'subnet': kwargs.get('forsubnetce'),
            'primary_ipv4_address': kwargs.get('primary_ipv4_address'),
            'security_groups': kwargs.get('security_groups'),
        }

        instance_info = self.get_instance(args["instance"])
        if "errors" in instance_info:
            return instance_info

        subnet_info = self.subnet.get_subnet(args["subnet"])
        if "errors" in subnet_info:
            return subnet_info

        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                if key == "security_groups":
                    sg = []
                    for key_sg in args["security_groups"]:
                        tmp_sg = {}
                        tmp_sg["id"] = key_sg
                        sg.append(tmp_sg)
                    payload["security_groups"] = sg
                elif key == "subnet":
                    payload["subnet"]: {"id": subnet_info["id"]}
                else:
                    payload[key] = value

        try:
            path = ("/v1/instances/{}/network_interfaces?version={}"
                    "&generation={}").format(instance_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating instance interface. {}").format(error)
            raise

    def associate_floating_ip(self, **kwargs):
        """
        Associate floating IP with a network interface
        :param instance: The instance name or ID.

        :param interface: The network interface name or ID

        :param fip: The floting IP name, ID or address
        """
        args = ["instance", "interface", "fip"]
        check_args(args, **kwargs)

        args = {
            'instance': kwargs.get('instance'),
            'interface': kwargs.get('interface'),
            'fip': kwargs.get('fip'),
        }

        instance_info = self.get_instance(args["instance"])
        if "errors" in instance_info:
            return instance_info

        interface_info = self.get_instance_interface(args["interface"])
        if "errors" in interface_info:
            return interface_info

        fip_info = self.fip.get_floating_ip(args["fip"])
        if "errors" in fip_info:
            return fip_info

        try:
            path = ("/v1/instances/{}/network_interfaces/{}/floating_ips/{}"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        interface_info["id"],
                                                        fip_info["id"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            return qw("iaas", "POST", path, headers(), None)["data"]

        except Exception as error:
            print("Error associating floating IP {} on network interface {}"
                  " for instance {}. {}").format(fip_info["id"],
                                                 interface_info["id"],
                                                 instance_info["id"], error)
            raise

    def attach_volume(self, **kwargs):
        """
        Attach a volume to an instance
        :param instance: The instance name or ID.

        :param volume: The identity of the volume to attach to the instance.

        :param delete_volume_on_instance_delete: Optional. If set to true, when
        deleting the instance the volume will also be deleted.

        :param name: Optional. The user-defined name for this volume
        attachment.
        """
        args = ["instance", "volume"]
        check_args(args, **kwargs)

        args = {
            'instance': kwargs.get('instance'),
            'volume': kwargs.get('volume'),
            'delete_volume_on_instance_delete': kwargs.get(
                'delete_volume_on_instance_delete'),
            'name': kwargs.get('name'),
        }

        instance_info = self.get_instance(args["instance"])
        if "errors" in instance_info:
            return instance_info

        volume_info = self.volume.get_volume(args["volume"])
        if "errors" in volume_info:
            return volume_info

        payload = {}
        for key, value in args.items():
            if key != "instance" and value is not None:
                if key == "volume":
                    payload["volume"] = {"id", volume_info["id"]}
                else:
                    payload[key] = value

        try:
            path = ("/v1/instances/{}/volume_attachments?version={}"
                    "&generation={}").format(instance_info["id"],
                                             self.cfg["version"],
                                             self.cfg["generation"])

            return qw("iaas", "POST", path, headers(),
                      json.dumps(payload))["data"]

        except Exception as error:
            print("Error creating volume attachment. {}").format(error)
            raise

    def delete_instance(self, instance):
        """
        Delete instance
        :param instance: Instance name or ID
        """
        try:
            instance_info = self.get_instance(instance)
            if "errors" in instance_info:
                return instance_info

            path = ("/v1/instances/{}?version={}&generation={}").format(
                instance_info["id"], self.cfg["version"],
                self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error deleting instance {}. {}").format(instance, error)
            raise

    def delete_instance_interface(self, instance, interface):
        """
        Delete interface from instance
        :param instance: Instance name or ID
        :param interface: Interface name or ID
        """
        try:
            instance_info = self.get_instance(instance)
            if "errors" in instance_info:
                return instance_info

            interface_info = self.get_instance_interface(interface)
            if "errors" in interface_info:
                return interface_info

            path = ("/v1/instances/{}?version={}&generation={}").format(
                instance_info["id"], interface_info["id"], self.cfg["version"],
                self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error deleting instance {}. {}").format(instance, error)
            raise

    def disassociate_floating_ip(self, instance, interface, fip):
        """
        Disassociate floating IP from a network interface on an instance
        :param instance: Instance name or ID
        :param interface: Interface name or ID
        :parem fip: Floating IP name, ID or address
        """
        try:
            instance_info = self.get_instance(instance)
            if "errors" in instance_info:
                return instance_info

            interface_info = self.get_instance_interface(interface)
            if "errors" in interface_info:
                return interface_info

            fip_info = self.fip.get_floating_ip(fip)
            if "errors" in fip_info:
                return fip_info

            path = ("/v1/instances/{}/network_interfaces/{}/floating_ips/{}"
                    "?version={}&generation={}").format(instance_info["id"],
                                                        interface_info["id"],
                                                        fip_info["id"],
                                                        self.cfg["version"],
                                                        self.cfg["generation"])

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error disassociating floating IP {} from network interface"
                  " {} on instance {}. {}").format(fip, interface, instance,
                                                   error)
            raise

    def detach_volume(self, instance, volume):
        """
        Detach volume from an instance
        :param instance: Instance name or ID
        :param volume: Volume name or ID
        """
        try:
            instance_info = self.get_instance(instance)
            if "errors" in instance_info:
                return instance_info

            volume_info = self.volume.get_volume(volume)
            if "errors" in volume_info:
                return volume_info

            path = ("/v1/instances/{}/volume_attachments/{}"
                    "?version={}&generation={}".format(instance_info["id"],
                                                       volume_info["id"],
                                                       self.cfg["version"],
                                                       self.cfg["generation"]))

            data = qw("iaas", "DELETE", path, headers())

            if data["response"].status != 204:
                return data["data"]

            return resource_deleted()

        except Exception as error:
            print("Error detaching volume {} from instance {}. {}".format(
                volume, instance, error))
            raise
