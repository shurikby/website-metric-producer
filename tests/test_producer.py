import unittest

from app.producer import get_website_metrics
from tests import app_factory
from config import integration_mode, target_website_simulator_url


class MyProducerTest(unittest.TestCase):
    app = None

    def setUp(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(self.app is None)
        self.app = app_factory.build_production_app()
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def tearDown(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def test_instance_type(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(isinstance(self.app, app_factory.Producer))

    def test_get_website_metrics(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        sample_time, status_code, elapsed_seconds, isFound = get_website_metrics('http://127.0.0.1:1234/')
        self.assertEqual(503, status_code)
        self.assertFalse(isFound)
        sample_time, status_code, elapsed_seconds, isFound = get_website_metrics(target_website_simulator_url)
        self.assertEqual(200, status_code)
        self.assertTrue(isFound)


if __name__ == '__main__':
    unittest.main()
