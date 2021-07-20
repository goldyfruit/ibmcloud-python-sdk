from os import CLD_CONTINUED
import os.path
import json
import re

from tests.Common import Common

class Authentication(Common):

    # token_file = open(Common.resource_path+'/authentication/token.jwt', mode='rb')
    # token = token_file.read()

    authentication_payload = {
        "access_token": "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaXRzX2libV9iYWJ5In0.DpusWTm59F6LiPCVIcVFtl4QgF1VKhqaMHg-_jeHkd4",
        "refresh_token": "not_supported",
        "ims_user_id": 8123932,
        "token_type": "Bearer",
        "expires_in": 3600,
        "expiration": 1626565349,
        "scope": "ibm openid"
    }

    @classmethod
    def get_headers(self):
        result = {}

        result["Authorization"] = "Bearer {}".format(
            self.authentication_payload["access_token"])
        return(result)

    @classmethod
    def decode(self, token, verify):
        result = {
            "iam_id": "IBMid-123456BVZU",
            "id": "IBMid-123456BVZU",
            "realmid": "IBMid",
            "jti": "d1b244d90-4c84-4345-9b61-befa17bd5fd8",
            "identifier": "123456BVZU",
            "given_name": "Unittest",
            "family_name": "User",
            "name": "Unittest User",
            "email": "unittest@example.com",
            "sub": "unittest@example.com",
            "authn": {
                "sub": "unittest@example.com",
                "iam_id": "IBMid-123456BVZU",
                "name": "Unittest User",
                "given_name": "Unittest",
                "family_name": "User",
                "email": "unittest@example.com"
            },
            "account": {
                "boundary": "global",
                "valid": "true",
                "bss": "8d143b8b90e135fd8ffe0e5e9c291c9d",
                "ims_user_id": "9236849",
                "frozen": "true",
                "ims": "2006826"
            },
            "iat": 1626561749,
            "exp": 1626565349,
            "iss": "https://iam.cloud.ibm.com/identity",
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "scope": "ibm openid",
            "client_id": "default",
            "acr": 1,
            "amr": [
                "pwd"
            ]
        }
        return (result)

    @classmethod
    def query_wrapper(self, service, verb, path, headers, payload):
        result = {}

        result["data"] = self.authentication_payload
        return(result)