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

    def test_get_event(self):
        EVENT = {
            "dates": [
                {
                    "day": 4,
                    "month": 2,
                    "times": {"1": {"end": 12, "start": 10}, "2": {"end": 23, "start": 22}},
                    "year": 2020,
                }
            ],
            "description": "first description",
            "title": "event 1",
        }
        response = self.app.get("/events/event 1")
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(EVENT, response.json)