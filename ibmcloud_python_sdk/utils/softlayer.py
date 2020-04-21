import SoftLayer
from ibmcloud_python_sdk.config import params


def client():
    """Create SoftLayer client

    :return: The SoftLayer client
    """
    cfg = params()

    try:
        client = SoftLayer.create_client_from_env(
            username=cfg['cis_username'],
            api_key=cfg['cis_apikey']
        )

        return client

    except Exception as error:
        print("Error creating softlayer client. {}".format(error))
        raise
