from tests.Common import Common

class FloatingIp(Common):

    json_content = Common.get_json_resource_content("floating_ips")

    name = json_content["floating_ips"][0]["name"]
    id = json_content["floating_ips"][0]["id"]
    address = json_content["floating_ips"][0]["address"]

    @classmethod
    def get_resource_group(self, fip):
        result = Common.get_resource_group("floating_ips")
        return(result["data"])


    @classmethod
    def reserve_floating_ip(self, service, verb, path, headers, payload):
        """
        This function will replace the original API.
        """
        # result = {}
        # result['data'] = {}
        # folder = self.set_folder(path)
        # resource_file = os.path.normpath('tests/resources/{}/{}.json').format(
        #     folder,
        #     folder
        # )
        # # Must return a file-like object
        # try:
        #     json_file = open(resource_file, mode='rb')
        #     result["data"] = json.load(json_file)
        #     print(result["data"])
        #     return(result)
        # except IOError:
        #     return result["data"][folder].append({"error": "not found"})
        #     raise
        pass
