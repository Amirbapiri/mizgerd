from flask import Response, request
from flask_restful import Resource, reqparse

events = []


class EventsAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True,
                        help="This filed can not be empty.")
    parser.add_argument("description", required=False)
    parser.add_argument("dates", required=True)

    """
    Retrieve a specific event based on title   
    """

    def get(self, title):
        """
        Retrieve a specific event based on title
        """
        event = next(filter(lambda e: e["title"] == title, events), None)
        return {"event": event}, 200 if event else 404

    def post(self):
        """
        Insert new event
        """
        data = EventsAPI.parser.parse_args()
        event = {
            "title": data["title"],
            "description": data["description"],
            "dates": data["dates"]
        }

        events.append(event)
        return event, 201


class EventList(Resource):
    """
    Retrieve list of events
    """

    def get(self):
        return events
