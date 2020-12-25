from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Event(Resource):
    def get(self):
        """
        Retrieve all events
        """
        return {"Event": "something new "}

    def post(self):
        """
        Insert new event
        """
        pass


api.add_resource(Event, "/event")

if __name__ == "__main__":
    app.run()
