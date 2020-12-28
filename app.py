from flask import Flask, jsonify, request, Response, json

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
    is_data_provided = ("title" in data and bool(data["title"])) and ("description" in data and bool(
        data["description"])) and ("dates" in data and bool(len(data["dates"])))
    if data and is_data_provided:
        events.append(data)
        return jsonify(data), 201
    else:
        return jsonify({"Detail": "'title', 'description' and 'dates' are required."}), 400
    return jsonify({"Detail": "Failed! something goes wrong here!"}), 400
