import unittest
import json

from app import app


class TestEvents(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create(self):
        payload = {
            "title": "TestTitle",
            "description": "TestDescription",
            "dates": [{"year": 2020, "month": 2, "day": 4, "times": {}}],
        }
        response = self.app.post(
            "/event",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        self.assertDictEqual(payload, response.json)
        self.assertEqual(201, response.status_code)

    def test_list_events(self):
        response = self.app.get("/events")
        self.assertEqual(200, response.status_code)
