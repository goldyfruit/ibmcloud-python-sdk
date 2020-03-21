import http.client
import os
from . import auth as ic


MANDATORY_ENV_VARS = ["IC_VERSION", "IC_API_KEY",
                      "IC_REGION", "IC_GENERATION"]


class Config():

    def __init__(self):
        for var in MANDATORY_ENV_VARS:
            if var not in os.environ:
                raise EnvironmentError(
                    f"Failed because {var} is not set.")

        auth = ic.Auth()
        self.version = os.environ.get("IC_VERSION")
        self.region = os.environ.get("IC_REGION")
        self.key = os.environ.get("IC_API_KEY")
        self.generation = os.environ.get("IC_GENERATION")
        self.authUrl = "iam.cloud.ibm.com"
        self.url = f"{self.region}.iaas.cloud.ibm.com"
        self.url_rg = "resource-controller.cloud.ibm.com"
        self.conn = http.client.HTTPSConnection(self.url)
        self.conn_rg = http.client.HTTPSConnection(self.url_rg)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': auth.get_token(self.authUrl, self.key),
        }
