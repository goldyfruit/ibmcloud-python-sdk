<<<<<<< HEAD
import http.client
import json
=======
from ibmcloud_python_sdk.utils import constants
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils import common

cfg = params()
headers = {}

>>>>>>> 8456b75 ([module] Improve setup.py)

def get_token(url, key):
    # Payload for retrieving token
    payload = ("grant_type=urn:ibm:params:oauth:grant-type:"
               "apikey&apikey={}").format(key)

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
        print(f"Error getting token. {error}")
        raise


def get_headers():
    if not headers:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["User-Agent"] = "IBM-Cloud_Python_SDK"
        headers["Authorization"] = get_token(constants.AUTH_URL, cfg["key"])

<<<<<<< HEAD
<<<<<<< HEAD
    # If an error happens while retrieving token
    except Exception as error:
        print(f"Error getting token. {error}")
        raise
=======
            # Concatenate token type and token value
            return json_res['token_type'] + ' ' + json_res['access_token']

        # If an error happens while retrieving token
        except Exception as error:
            print(f"Error getting token. {error}")
            raise
>>>>>>> 5410cdd ([git] Ignore .vscode directory)
=======
        return headers

    return headers
>>>>>>> 8456b75 ([module] Improve setup.py)
