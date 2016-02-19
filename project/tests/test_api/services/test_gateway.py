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
import websocket

from test_utils import ApiTestCase, cleanup_after_failed_setup, CfApiClient
from objects import Organization, ServiceInstance, User, Application, ServiceBinding


class Gateway(ApiTestCase):
    LABEL = "gateway"
    KAFKA_LABEL = "kafka"
    PLAN_NAME = "Simple"
    gateway_instance = None
    kafka_instance = None
    gateway_app = None

    @classmethod
    @cleanup_after_failed_setup(User.cf_api_tear_down_test_users, Organization.cf_api_tear_down_test_orgs)
    def setUpClass(cls):
        cls.step("Create test organization and test space")
        cls.test_org = Organization.api_create(space_names=("test-space",))
        cls.test_space = cls.test_org.spaces[0]
        cls.step("Create space developer client")
        space_developer_user = User.api_create_by_adding_to_space(cls.test_org.guid, cls.test_space.guid,
                                                                  roles=User.SPACE_ROLES["developer"])
        cls.space_developer_client = space_developer_user.login()
        cls.step("Retrieve oauth token")
        cf_api_client = CfApiClient.get_client()
        cls.token = cf_api_client.get_oauth_token()

    @ApiTestCase.mark_prerequisite(is_first=True)
    def test_0_create_gateway_instance(self):
        self.step("Create gateway instance")
        self.__class__.gateway_instance = ServiceInstance.api_create(self.test_org.guid, self.test_space.guid,
                                                                     self.LABEL, service_plan_name=self.PLAN_NAME,
                                                                     client=self.space_developer_client)
        self.step("Check that instance was created")
        self.assertInListWithRetry(self.gateway_instance, ServiceInstance.api_get_list, self.test_space.guid)
        app_list = Application.api_get_list(self.test_space.guid)
        self.__class__.gateway_app = next((app for app in app_list if app.name.startswith(self.gateway_instance.name)),
                                          None)
        self.assertIsNotNone(self.gateway_app, "Gateway app not found")
        self.gateway_app.ensure_started()
        self.step("Check bound kafka instance")
        bound_services = ServiceBinding.api_get_list(self.gateway_app.guid)
        self.assertEqual(len(bound_services), 1, "Found more than one binding")
        service_list = ServiceInstance.api_get_list(self.test_space.guid)
        self.__class__.kafka_instance = next((si for si in service_list
                                              if si.guid == bound_services[0].service_instance_guid), None)
        self.assertIsNotNone(self.kafka_instance, "Bound kafka service instance not found")
        self.assertEqual(self.kafka_instance.service_label, self.KAFKA_LABEL,
                         "Gateway app is not bound to kafka instance")

    @ApiTestCase.mark_prerequisite()
    def test_1_send_message_to_gateway_app_instance(self):
        self.step("Check communication with gateway app")
        header = ["Authorization: Bearer{}".format(self.token)]
        try:
            websocket.enableTrace(True)
            ws = websocket.WebSocket()
            ws.connect("ws://{}/ws".format(self.gateway_app.urls[0]), header=header)
            ws.send("test")
            ws.close()
        except websocket.WebSocketException as e:
            raise AssertionError(str(e))

    @ApiTestCase.mark_prerequisite()
    def test_2_delete_gateway_instance(self):
        self.step("Delete gateway instance")
        self.gateway_instance.api_delete(client=self.space_developer_client)
        self.assertNotInListWithRetry(self.gateway_instance, ServiceInstance.api_get_list, self.test_space.guid)
        self.step("Check that bound kafka instance was also deleted")
        service_instances = ServiceInstance.api_get_list(self.test_space.guid)
        self.assertNotInList(self.kafka_instance, service_instances, "Kafka instance was not deleted")