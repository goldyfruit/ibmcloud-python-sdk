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
    option["em_url"] = constants.EM_URL
    option["sl_url"] = constants.SL_URL
    option["http_timeout"] = constants.HTTP_TIMEOUT

    if path.isfile(creds):
        with open(creds, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError as error:
                print("Error reading config file: {}. {}".format(creds, error))
                return
    else:
        for var in constants.MANDATORY_ENV_VARS:
            if var not in environ:
                raise EnvironmentError(
                    "Failed because {} global variable is not set.".format(
                        var))

        option["version"] = environ.get("IC_VERSION")
        option["region"] = environ.get("IC_REGION")
        option["generation"] = environ.get("IC_GENERATION")
        option["key"] = environ.get("IC_API_KEY")
        if "SL_USERNAME" in environ and "SL_API_KEY" in environ:
            option["cis_username"] = environ.get("SL_USERNAME")
            option["cis_apikey"] = environ.get("SL_API_KEY")
        option["is_url"] = "{}.{}".format(
            environ.get("IC_REGION"), constants.IS_URL)

        return option

    if "default" in config["clouds"]:
        cloud = config["clouds"][config["clouds"]["default"]]
    else:
        if "IC_CONFIG_NAME" in environ:
            cloud = config["clouds"][environ.get("IC_CONFIG_NAME")]
        else:
            raise Exception("Configuration name should be defined.")

    option["version"] = cloud["version"]
    option["region"] = cloud["region"]
    option["generation"] = cloud["generation"]
    option["key"] = cloud["key"]
    if "cis_username" in cloud and "cis_apikey" in cloud:
        option["cis_username"] = cloud["cis_username"]
        option["cis_apikey"] = cloud["cis_apikey"]
    option["is_url"] = "{}.{}".format(cloud["region"], constants.IS_URL)
    option["pi_url"] = "{}.{}".format(cloud["region"], constants.PI_URL)

    return option


def sdk():
    sdk_config = "{}/.ibmcloud/sdk.yaml".format(environ.get('HOME'))
    config = None
    if "IC_SDK_CONFIG_FILE" in environ:
        sdk_config = environ.get("IC_SDK_CONFIG_FILE")

    if path.isfile(sdk_config):
        with open(sdk_config, "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
            except yaml.YAMLError as error:
                print("Error reading sdk.yaml file: {}. {}".format(
                    sdk_config, error))
                return False

    if config:
        options = {}
        for option, value in config["sdk"].items():
            options[option] = value

        return options

    return False
