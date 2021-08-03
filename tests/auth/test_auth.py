import json
import os
from unittest import TestCase
from mock import patch
from ibmcloud_python_sdk.utils import constants
from ibmcloud_python_sdk.auth import decode_token, get_token
from tests.common import get_headers, qw_exception


class AuthTestCase(TestCase):
    def read_token():
        """This function returns a generated JSON token.
        """
        data_file = f'{os.path.dirname(__file__)}/token.json'
        with open(data_file, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError as err:
                return err

    def read_decode(token, verify):
        """This function returns a decoded JSON token.
        """
        data_file = f'{os.path.dirname(__file__)}/decode.json'
        with open(data_file, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError as err:
                return err

    def qw(arg1, arg2, path, headers=None, payload=None):
        """This function is used to mock the query_wrapper function from
        utils/common. It returns information collected from read_token()
        function.
        """
        return {'data': AuthTestCase.read_token()}

    @patch('ibmcloud_python_sdk.auth.get_headers', get_headers)
    @patch('ibmcloud_python_sdk.auth.decode', read_decode)
    def test_decode_token(self):
        response = decode_token()
        self.assertEqual(response['given_name'], 'Unittest')

    @patch('ibmcloud_python_sdk.auth.get_headers', qw_exception)
    @patch('ibmcloud_python_sdk.auth.decode', read_decode)
    def test_decode_token_exception(self):
        with self.assertRaises(Exception):
            decode_token()

    @patch('ibmcloud_python_sdk.utils.common.query_wrapper', qw)
    def test_get_token(self):
        response = get_token(
            constants.AUTH_URL,
            '60230291428a3576752104555fa0f623b5045f08'
        )
        self.assertEqual(response,
                         f'Bearer {AuthTestCase.read_token()["access_token"]}')

    @patch('ibmcloud_python_sdk.utils.common.query_wrapper', qw_exception)
    def test_get_token_exception(self):
        with self.assertRaises(Exception):
            get_token(constants.AUTH_URL,
            '60230291428a3576752104555fa0f623b5045f08'
        )