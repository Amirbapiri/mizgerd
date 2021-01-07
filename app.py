from flask import Flask, jsonify, request

app = Flask(__name__)

events = [
    {
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
]


@app.route("/event", methods=["POST"])
def create_event():
    data = request.json
    is_data_provided = (
        ("title" in data and bool(data["title"]))
        and ("description" in data and bool(data["description"]))
        and ("dates" in data and bool(len(data["dates"])))
    )
    if data and is_data_provided:
        events.append(data)
        return jsonify(data), 201
    else:
        return (
            jsonify({"Detail": "'title', 'description' and 'dates' are required."}),
            400,
        )


@app.route("/events", methods=["GET"])
def list_events():
    return jsonify(events), 200


@app.route("/events/<string:title>", methods=["GET"])
def get_event(title):
    res = next(iter(filter(lambda x: x["title"] == title, events) or []), None)
    if res:
        return jsonify(res), 200
    return jsonify({"Detail": "Couldn't find any event with given 'title'."}), 400


@app.route("/events/<string:title>", methods=["PUT"])
def update_event(title):
    data = request.json
    if data:
        res = next(iter(filter(lambda x: x["title"] == title, events) or []), None)
        if res:
            res.update(
                title=data["title"] if "title" in data else res["title"],
                description=data["description"]
                if "description" in data
                else res["description"],
            )
            return jsonify(res), 200
        return jsonify({"Detail": "Couldn't find any event with the given 'title'"})
    return jsonify({"Detail": "Error!"})


@app.route("/events/<string:title>", methods=["DELETE"])
def delete_event(title):
    global events
    events = list(filter(lambda x: x["title"] != title, events))
    return "", 204
