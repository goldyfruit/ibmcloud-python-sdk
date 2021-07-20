import unittest

from mock import patch

from ibmcloud_python_sdk.auth import (
    decode_token,
    get_token,
    get_headers,
)

from tests.Authentication import Authentication
from tests.Common import Common


class AuthenticationTestCase(unittest.TestCase):
    """Test case for the client methods."""

    # def setUp(self) -> None:
    #     self.auth = Authentication

    # def tearDown(self):
    #     self.patcher.stop()

    @patch('ibmcloud_python_sdk.auth.get_headers', Authentication.get_headers)
    @patch('ibmcloud_python_sdk.auth.decode', Authentication.decode)
    def test_get_decode_token(self):
        """ Test decode_token"""
        response = decode_token()
        self.assertNotEqual(len(response), 0)

    @patch('ibmcloud_python_sdk.auth.get_headers', Authentication.return_exception)
    @patch('ibmcloud_python_sdk.auth.decode', Authentication.decode)
    def test_get_decode_token_error_by_exception(self):
        """ Test decode_token (error by exception)"""
        with self.assertRaises(Exception):
            response = decode_token()

    @patch('ibmcloud_python_sdk.utils.common.query_wrapper', Authentication.query_wrapper)
    # @patch('ibmcloud_python_sdk.auth.decode', Authentication.decode)
    def test_get_token(self):
        """ Test get_token"""
        response = get_token("my_url",
        "my-key")
        self.assertEqual(response, "Bearer {}".format(
            Authentication.authentication_payload["access_token"]))

    @patch('ibmcloud_python_sdk.utils.common.query_wrapper', Authentication.return_exception)
    def test_get_token_error_by_exception(self):
        """ Test get_token (error by exception)"""
        with self.assertRaises(Exception):
            response = get_token("my_url",
                "my-key")

    # def test_get_headers(self):
    #     """ Test get_headers"""
    #     response = get_headers