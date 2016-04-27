#
# Copyright (c) 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest
from unittest import mock

from .mock_dynamic_config import mock_dynamic_config
from .mock_http_session import MockHttpSession
from modules.http_client.client_auth.client_auth_token_basic import ClientAuthTokenBasic
from modules.http_client.client_auth.client_auth_token_uaa import ClientAuthTokenUaa
from modules.http_client.client_auth.client_auth_type import ClientAuthType
from modules.http_client.client_auth.client_auth_factory import ClientAuthFactory, \
    ClientAuthFactoryInvalidAuthTypeException


@mock.patch("modules.http_client.client_auth.client_auth_token_uaa.dynamic_config", mock_dynamic_config)
class TestClientAuthFactory(MockHttpSession):
    """Unit: ClientAuthFactory."""

    USERNAME = "username"
    PASSWORD = "password"

    def setUp(self):
        self.mock_http_session()
        super().setUp()

    def test_get_should_return_auth_token_basic(self):
        self._assertClientAuthInstance(ClientAuthType.TOKEN_BASIC, ClientAuthTokenBasic)

    def test_get_should_return_auth_token_uaa(self):
        self._assertClientAuthInstance(ClientAuthType.TOKEN_UAA, ClientAuthTokenUaa)

    def test_get_should_return_auth_http_basic(self):
        self.assertRaises(
            NotImplementedError,
            ClientAuthFactory.get,
            self.USERNAME,
            self.PASSWORD,
            ClientAuthType.HTTP_BASIC
        )

    def test_get_should_return_auth_login_page(self):
        self.assertRaises(
            NotImplementedError,
            ClientAuthFactory.get,
            self.USERNAME,
            self.PASSWORD,
            ClientAuthType.LOGIN_PAGE
        )

    def test_get_should_return_exception_for_undefined_type(self):
        self.assertRaises(
            ClientAuthFactoryInvalidAuthTypeException,
            ClientAuthFactory.get,
            self.USERNAME,
            self.PASSWORD,
            "UndefinedType"
        )

    def _assertClientAuthInstance(self, auth_type, clazz):
        auth = ClientAuthFactory.get(self.USERNAME, self.PASSWORD, auth_type)
        self.assertIsInstance(auth, clazz, "Invalid auth class.")


if __name__ == '__main__':
    unittest.main()