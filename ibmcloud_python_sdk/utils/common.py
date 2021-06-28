import base64
import http.client
import json
from jwt import decode
from ibmcloud_python_sdk.config import params
from ibmcloud_python_sdk.utils import cache


def _account_id(headers):
    """Retrieve BSS ID and encode it to base64

    :param headers: Headers to parse
    :type headers: dict
    :return: BSS ID encoded to base64
    :rtype: str
    """
    auth = headers.get("Authorization")
    if auth:
        # Split the Bearer token and decode the JWT
        jwt = decode(auth.split(" ")[1], verify=False)

        # Encode BSS ID to base64
        encoded = base64.b64encode(jwt["account"]["bss"].encode("utf-8"))

        # Returns base64 string
        return encoded.decode()


def query_wrapper(conn_type, method, path, headers=None, payload=None):
    """Execute HTTP query and return JSON response

    :param conn_type: Define which URL should be used for the connection
        such as "iaas", "auth", "cis", or "rg" (resource group)
    :type conn_type: str
    :param method: HTTP method that should be used such as
        GET, POST, PUT, DELETE, etc...
    :type method: str
    :param path: Path used by within the query
    :type path: str
    :param headers: Headers to send with the query is required such
        authentication token, content type, etc...
    :type headers: dict, optional
    :param payload: JSON payload send during the query
    :type payload: dict, optional
    :return: JSON response
    :rtype: dict
    """
    cfg = params()
    timeout = cfg["http_timeout"]

    if conn_type == "iaas":
        conn = http.client.HTTPSConnection(cfg["is_url"], timeout=timeout)
    elif conn_type == "rg":
        conn = http.client.HTTPSConnection(cfg["rg_url"], timeout=timeout)
    elif conn_type == "auth":
        conn = http.client.HTTPSConnection(cfg["auth_url"], timeout=timeout)
    elif conn_type == "dns":
        conn = http.client.HTTPSConnection(cfg["dns_url"], timeout=timeout)
    elif conn_type == "em":
        conn = http.client.HTTPSConnection(cfg["em_url"], timeout=timeout)
    elif conn_type == "sl":
        if headers and cfg["cis_username"] and cfg["cis_apikey"]:
            header = base64.encodebytes(
                ('%s:%s' % (cfg["cis_username"], cfg["cis_apikey"]))
                .encode('utf8')).decode('utf8').replace('\n', '')
            headers["Authorization"] = "Basic {}".format(header)
        conn = http.client.HTTPSConnection(cfg["sl_url"], timeout=timeout)
    elif conn_type == "power":
        conn = http.client.HTTPSConnection(cfg["pi_url"], timeout=timeout)

    if cache.client():
        if method == "GET" and conn_type != "auth":
            obj = "{}{}".format(_account_id(headers), path)
            item = cache.get_item(obj)
            if item is not None:
                return {"data": json.loads(item.decode("utf-8"))}
            else:
                pass

    conn.request(method, path, payload, headers)

    # Get and read response data
    res = conn.getresponse()
    data = res.read()

    if not data:
        # Return empty data and HTTP response this is mostly
        # due to DELETE request which doesn't return any data
        return {"data": None, "response": res}
    else:
        if cache.client():
            obj = "{}{}".format(_account_id(headers), path)
            # Store item into caching system
            cache.set_item(obj, data)

        # Return data and HTTP response
        return {"data": json.loads(data), "response": res}


def check_args(arguments, **kwargs):
    """Check that required arguments are passed to the function

    :param arguments: List of required arguments
    :type arguments: list
    """
    # Argument required by the function
    required = set(arguments)

    # Argument passed to the function
    passed = set(kwargs.keys())

    # Check if required arguments are passed
    if not required.issubset(passed):
        raise KeyError(
            "Required param(s) is/are missing. Required: {}".format(required)
        )


def resource_not_found(payload=None):
    """Return custom JSON if a resource is not found

    :param payload: Customize the JSON to return if needed
    :type payload: dict, optional
    :return: A JSON dict with a message
    :rtype: dict
    """
    if payload is not None:
        return payload
    else:
        return {"errors": [{"code": "not_found"}]}


def resource_deleted(payload=None):
    """Return custom JSON if a resource is deleted

    :param payload: Customize the JSON to return if needed
    :type payload: dict, optional
    :return: A JSON dict with a message
    :rtype: dict
    """
    if payload is not None:
        return payload
    else:
        return {"status": "deleted"}


def resource_found(payload=None):
    """Return custom JSON if a resource is found but doesn't have output

    :param payload: Customize the JSON to return if needed
    :type payload: dict, optional
    """
    if payload is not None:
        return payload
    else:
        return {"status": "found"}


def resource_created(payload=None):
    """Return custom JSON if a resource is created but doesn't have output

    :param payload: Customize the JSON to return if needed
    :type payload: dict, optional
    :return: A JSON dict with a message
    :rtype: dict
    """
    if payload is not None:
        return payload
    else:
        return {"status": "created"}


def resource_error(code, message):
    """Return custom JSON if a resource raised an exception. This will be
        mostly used during try: / except: on SoftLayer resources

    :param code: Code to return
    :type code: int
    :param message: Message to return
    :type messaage: str
    :return: A JSON dict with an error message
    :rtype: dict
    """
    if code == 404:
        code = "not_found"
    return {"errors": {"code": code, "message": message}}
