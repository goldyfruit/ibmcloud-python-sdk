import SoftLayer
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils import constants


def client():
    """Create SoftLayer client

    :return: The SoftLayer client
    """
    cfg = params()
    endpoint_url = "https://{}/rest/v3.1/".format(constants.SL_URL)
    try:
        client = SoftLayer.create_client_from_env(
            username=cfg['cis_username'],
            api_key=cfg['cis_apikey'],
            endpoint_url=endpoint_url,
        )

        return client

    except SoftLayer.SoftLayerError as error:
        print("Error creating SoftLayer client. {}".format(error))
        raise
