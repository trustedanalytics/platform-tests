import unittest

from test_utils import ApiTestCase
from test_utils.objects import Organization, ServiceInstance


class MetricsTest(ApiTestCase):

    @classmethod
    def setUpClass(cls):
        cls.seedorg = Organization.get_seedorg()
        cls.seedorg.api_get_metrics()

    @unittest.expectedFailure
    def test_service_count(self):
        cf_api_service_instances = ServiceInstance.cf_api_get_service_instances(self.seedorg.guid)
        self.assertEqual(self.seedorg.metrics["service_usage"], len(cf_api_service_instances))

