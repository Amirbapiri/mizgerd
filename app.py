from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

events = []


class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True,
                        help="This filed can not be empty.")
    parser.add_argument("description", required=False)
    parser.add_argument("dates", required=True)

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
        data = Event.parser.parse_args()
        event = {
            "title": data["title"],
            "description": data["description"],
            "dates": data["dates"],
        }
        events.append(event)
        return event, 201


class EventList(Resource):
    def get(self):
        return events


api.add_resource(Event, "/event", "/event/<string:title>")
api.add_resource(EventList, "/event/list")

if __name__ == "__main__":
    app.run()
