from ibmcloud_python_sdk.utils import constants
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils import common
from jwt import decode

cfg = params()
headers = {}


def decode_token():
    """Decode JWT token

    :return: JSON JWT information
    :rtype: dict
    """
    try:
        token = get_headers()["Authorization"]
        return decode(token.split(" ")[1], verify=False)

    except Exception as error:
        print("Error decoding token. {}".format(error))
        raise


def get_token(url, key):
    """Generate JWT IAM token

    :param url: IAM URL
    :type url: string
    :param key: API Key
    :type key: string
    :return: IAM token
    :rtype: string
    """
    # Payload for retrieving token
    payload = ("grant_type=urn:ibm:params:oauth:grant-type:"
               "apikey&apikey={}".format(key))

    # Required headers
    headers_auth = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    try:
        # Retrieve data
        data = common.query_wrapper("auth", "POST", "/identity/token",
                                    headers_auth, payload)["data"]

        # Concatenate token type and token value
        return data['token_type'] + ' ' + data['access_token']

    # If an error happens while retrieving token
    except Exception as error:
        print("Error getting token. {}".format(error))
        raise


def get_headers():
    """Generates the headers used for authenticated HTTP request.

    :return: Dict of headers
    :rtype: dict
    """
    if not headers:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["User-Agent"] = constants.USER_AGENT
        headers["Authorization"] = get_token(constants.AUTH_URL, cfg["key"])

        return headers

    return headers
