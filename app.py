from flask import Flask, jsonify, request, Response

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


@app.route("/event", methods=["POST"])
def create_event():
    data = request.json
    if data:
        if (not "title" in data) or (not "description" in data) or (not "dates" in data):
            return jsonify({"Detail": "'title', 'description' and 'dates' are required."}), 400
        else:
            if data["title"] and data["description"] and data["dates"]:
                events.append(data)
                return jsonify(data), 201
            else:
                return jsonify({"Detail": "'title', 'description' or dates can't be left blank."}), 400
    return jsonify({"Detail": "Failed! proper data must be provided."}), 400
