import http.client
import json
import os
from .auth import get_token


MANDATORY_ENV_VARS = ["IC_VERSION", "IC_API_KEY", "IC_REGION", "IC_GENERATION"]

for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError(f"Failed because {var} is not set.")

version = os.environ.get("IC_VERSION")
region = os.environ.get("IC_REGION")
key = os.environ.get("IC_API_KEY")
generation = os.environ.get("IC_GENERATION")
authUrl = "iam.cloud.ibm.com"
url = f"{region}.iaas.cloud.ibm.com"

conn = http.client.HTTPSConnection(url)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': get_token(authUrl, key),
}


