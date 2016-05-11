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

import os

from modules.api_client import PlatformApiClient


def api_create_transfer_by_file_upload(org_guid, source, category=None, is_public=None, title=None, client=None):
    """POST /rest/upload/{org_id}"""
    body_keys = ["category", "publicRequest", "orgUUID", "title"]
    values = [category, is_public, org_guid, title]
    data = {key: val for key, val in zip(body_keys, values) if val is not None}
    _, file_name = os.path.split(source)
    files = {"file": (file_name, open(source, "rb"), "application/vnd.ms-excel")}
    client = client or PlatformApiClient.get_admin_client()
    return client.request("POST", "rest/upload/{}".format(org_guid), data=data, log_msg="PLATFORM: create a transfer",
                          files=files)