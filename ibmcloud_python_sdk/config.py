from ibmcloud_python_sdk.utils import constants
from os import environ, path
import yaml


def params():
    creds = "{}/.ibmcloud/clouds.yaml".format(environ.get('HOME'))
    if "IC_CONFIG_FILE" in environ:
        creds = environ.get("IC_CONFIG_FILE")

    option = {}
    option["auth_url"] = constants.AUTH_URL
    option["dns_url"] = constants.DNS_URL
    option["rg_url"] = constants.RG_URL

    if path.exists(creds):
        with open(creds, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError as error:
                print(f"Error reading config file: {creds}. {error}")
    else:
        for var in constants.MANDATORY_ENV_VARS:
            if var not in environ:
                raise EnvironmentError(
                    f"Failed because {var} global variable is not set.")

        option["version"] = environ.get("IC_VERSION")
        option["region"] = environ.get("IC_REGION")
        option["generation"] = environ.get("IC_GENERATION")
        option["key"] = environ.get("IC_API_KEY")
        option["is_url"] = "{}.{}".format(
            environ.get("IC_REGION"), constants.IS_URL)

        return option

    if "default" in config["clouds"]:
        cloud = config["clouds"][config["clouds"]["default"]]
    else:
        if "IC_CONFIG_NAME" in environ:
            cloud = config["clouds"][environ.get("IC_CONFIG_NAME")]
        else:
            raise Exception(f"Configuration name should be defined.")

    option["version"] = cloud["version"]
    option["region"] = cloud["region"]
    option["generation"] = cloud["generation"]
    option["key"] = cloud["key"]
    option["is_url"] = "{}.iaas.cloud.ibm.com".format(cloud["region"])

    return option
