from flask import Flask, jsonify, request

app = Flask(__name__)

events = [
    {
        "dates": [
            {
                "day": 4,
                "month": 2,
                "times": {
                    "1": {
                        "end": 12,
                        "start": 10
                    },
                    "2": {
                        "end": 23,
                        "start": 22
                    }
                },
                "year": 2020
            }
        ],
        "description": "first description",
        "title": "event 1"
    }
]


@app.route("/events/new", methods=["POST"])
def create_event():
    data = request.json
    events.append(data)
    return jsonify(events), 201
