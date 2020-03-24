import http.client
import json
from . import config as ic


class Common():

    def __init__(self):
        self.cfg = ic.Config()

    def query_wrapper(self, conn_type, method, path, headers=None,
                      payload=None):
        """Execute HTTP query and return JSON response.
        :param conn_type: Define which URL should be used for the connection
            such as "iaas", "auth" or "rg" (resource group).
        :param method: HTTP method that should be used such as
            GET, POST, PUT, DELETE, etc...
        :param path: Path used by within the query
        :param headers: Optional. Headers to send with the query is required
            such authentication token, content type, etc...
        :param payload: Optional. JSON payload send during the query.
        """
        if conn_type == "iaas":
            self.conn = http.client.HTTPSConnection(self.cfg.url)
        elif conn_type == "rg":
            self.conn = http.client.HTTPSConnection(self.cfg.url_rg)
        elif conn_type == "auth":
            self.conn = http.client.HTTPSConnection(self.cfg.authUrl)

        self.conn.request(method, path, payload, headers)

        # Get and read response data
        res = self.conn.getresponse()
        data = res.read()

        if not data:
            # Return empty data and HTTP response this is mostly
            # due to DELETE request which doesn't return any data
            return {"data": None, "response": res}
        else:
            # Return data and HTTP response
            return {"data": json.loads(data), "response": res}
