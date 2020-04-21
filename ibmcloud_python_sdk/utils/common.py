import base64
import http.client
import json
from ibmcloud_python_sdk.config import params


def query_wrapper(conn_type, method, path, headers=None, payload=None):
    """Execute HTTP query and return JSON response.
    :param conn_type: Define which URL should be used for the connection
        such as "iaas", "auth", "cis", or "rg" (resource group).
    :param method: HTTP method that should be used such as
        GET, POST, PUT, DELETE, etc...
    :param path: Path used by within the query
    :param headers: Optional. Headers to send with the query is required
        such authentication token, content type, etc...
    :param payload: Optional. JSON payload send during the query.
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

    conn.request(method, path, payload, headers)

    # Get and read response data
    res = conn.getresponse()
    data = res.read()

    if not data:
        # Return empty data and HTTP response this is mostly
        # due to DELETE request which doesn't return any data
        return {"data": None, "response": res}
    else:
        # Return data and HTTP response
        return {"data": json.loads(data), "response": res}


def check_args(arguments, **kwargs):
    """Check that required arguments are passed to the function.
    :param arguments: List of required arguments.
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
    """Return custom JSON if a resource is not found.
    :param payload: Optional. Customize the JSON to return is needed.
    """
    if payload is not None:
        return payload
    else:
        return {"errors": [{"code": "not_found"}]}


def resource_deleted(payload=None):
    """Return custom JSON if a resource is deleted.
    :param payload: Optional. Customize the JSON to return is needed.
    """
    if payload is not None:
        return payload
    else:
        return {"status": "deleted"}


def resource_found(payload=None):
    """Return custom JSON if a resource is found but doesn't have output.
    :param payload: Optional. Customize the JSON to return is needed.
    """
    if payload is not None:
        return payload
    else:
        return {"status": "found"}


def resource_created(payload=None):
    """Return custom JSON if a resource is created but doesn't have output.
    :param payload: Optional. Customize the JSON to return is needed.
    """
    if payload is not None:
        return payload
    else:
        return {"status": "created"}
