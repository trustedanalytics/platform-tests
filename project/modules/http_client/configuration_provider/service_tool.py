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

from ..http_client_configuration import HttpClientConfiguration
from ..http_client_type import HttpClientType


class ServiceToolConfigurationProvider(object):
    """Provide configuration for service tool http client."""

    @classmethod
    def get(cls, url, username=None, password=None) -> HttpClientConfiguration:
        """Return http client configuration."""
        return HttpClientConfiguration(
            client_type=HttpClientType.SERVICE_TOOL,
            url=cls._prepare_url(url),
            username=username,
            password=password,
        )

    @staticmethod
    def _prepare_url(url):
        if not url.startswith("http"):
            url = "http://{}".format(url)
        return url
