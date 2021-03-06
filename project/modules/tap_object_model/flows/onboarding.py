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

from .. import Invitation, Organization, User
from ... import gmail_api
from ...constants import HttpStatus
from ...exceptions import UnexpectedResponseError
from ...http_calls.platform import user_management as api
from ...http_client.configuration_provider.console_no_auth import ConsoleNoAuthConfigurationProvider
from ...http_client.http_client_factory import HttpClientFactory
from ...test_names import generate_test_object_name


def onboard(context, username=None, password=None, org_name=None, inviting_client=None, check_email=True):
    """
    Onboard new user. Check email for registration code and register.
    Returns objects for newly created user and org.
    """
    password = User.generate_password() if password is None else password
    invitation = Invitation.api_send(context, username, inviting_client=inviting_client)
    if check_email:
        code = gmail_api.get_invitation_code_for_user(username=invitation.username)
    else:
        code = invitation.code
    return register(context, code, invitation.username, password, org_name)


def register(context, code, username, password=None, org_name=None):
    """
    Set password for new user and select name for their organization.
    Returns objects for newly created user and org.
    """
    password = User.generate_password() if password is None else password
    org_name = generate_test_object_name() if org_name is None else org_name
    client = HttpClientFactory.get(ConsoleNoAuthConfigurationProvider.get(username))
    try:
        response = api.api_register_new_user(code, password, org_name, client=client)
    except UnexpectedResponseError as e:
        # If exception occurred, other than conflict, check whether org and user are on the list and if so, delete it.
        if e.status != HttpStatus.CODE_CONFLICT:
            user = next((u for u in User.cf_api_get_all_users() if u.username == username), None)
            if user is not None:
                user.cleanup()
            org = next((o for o in Organization.api_get_list() if o.name == org_name), None)
            if org is not None:
                org.cleanup()
        raise
    new_org = Organization(name=response["org"], guid=response["orgGuid"])
    new_user = User(guid=response["userGuid"], username=username, password=response["password"],
                    org_roles={new_org.guid: ["managers"]})  # user is an org manager in the organization they create
    context.orgs.append(new_org)
    context.users.append(new_user)
    return new_user, new_org
