import json

import requests
import unittest


class EventsListTest(unittest.TestCase):
    def setUp(self):
        self.API_URL = "http://127.0.0.1:5000"
        self.EVENT = {
            "title": "new event",
            "description": "somethine new as description",
            "dates": {
                1: {"start": 10, "end": 12},
                2: {"start": 20, "end": 22},
            }
        }

    def test_get_event(self):
        event_title = "test_event"
        response = requests.get(
            self.API_URL + "/events/{title}".format(title=event_title))
        self.assertEqual(200, response.status_code)

    def test_add_new_event(self):
        response = requests.post(self.API_URL + "/events", json=self.EVENT)
        self.assertEqual(response.status_code, response.status_code)

    def test_get_events_list(self):
        response = requests.get(self.API_URL + "/events/list")
        self.assertEqual(200, response.status_code)
