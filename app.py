import os

from flask import Flask, jsonify, request, render_template

from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.environ.get("eusr")
app.config["MAIL_PASSWORD"] = "upiubmmkfubmrhab"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app=app)

events = [
    {
        "dates": {
            "1": {
                "day": 4,
                "month": 2,
                "times": {
                    "1": {"end": 12, "start": 11, "votes": 0},
                    "2": {"end": 24, "start": 23, "votes": 0},
                },
                "year": 2020,
            },
            "2": {
                "day": 12,
                "month": 2,
                "times": {
                    "1": {"end": 16, "start": 14, "votes": 0},
                    "2": {"end": 19, "start": 17, "votes": 0},
                },
                "year": 2020,
            },
        },
        "description": "first description",
        "title": "event 1",
        "is_finished": False,
    }
]

users = []

sessions = []


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
                description=data["description"] if "description" in data else res["description"],
            )
            return jsonify(res), 200
        return jsonify({"Detail": "Couldn't find any event with the given 'title'"})
    return jsonify({"Detail": "Error!"})


@app.route("/events/<string:title>", methods=["DELETE"])
def delete_event(title):
    global events
    events = list(filter(lambda x: x["title"] != title, events))
    return "", 204


@app.route("/events/<string:title>/finish", methods=["PUT"])
def finish_vote(title):
    res = next(iter(filter(lambda x: x["title"] == title, events) or []), None)
    if res:
        res.update(is_finished=True)
        return jsonify(res), 200
    return jsonify({"Detail": "Couldn't finish voting. 'title' is required."}), 400


@app.route("/events/<string:title>/<int:date_id>/<int:time_id>/vote", methods=["PUT"])
def vote_event(title, date_id, time_id):
    res = next(
        iter(filter(lambda x: x["title"] == title, events) or []),
        None,
    )
    if res:
        selected_time = res["dates"][str(date_id)]["times"][str(time_id)]
        if not res["is_finished"]:
            selected_time.update(votes=selected_time["votes"] + 1)
            return jsonify(res), 200
        return jsonify({"Detail": "Voting is over. You can't vote anymore."}), 400
    return jsonify({"Detail": "Couldn't find any event with given 'title'"}), 400


def find_event(title):
    event = next(iter(filter(lambda x: x["title"] == title, events) or []), None)
    if event:
        return event
    else:
        return None


def send_email(most_voted_object):
    msg = Message("Hello", sender=os.environ.get("eusr"), recipients=[os.environ.get("recipient")])
    msg.html = render_template("email_template.html", obj=most_voted_object["detail"])
    mail.send(msg)


@app.route("/events/<string:title>/mail", methods=["POST"])
def mail_most_voted(title):
    event = find_event(title)
    if event:
        most_voted_object = {}
        if not event["is_finished"]:
            return jsonify({"Detail": "Voting is not over yet!"}), 404
        dates = event["dates"]
        max_voted = 0
        for dates_key in dates.keys():
            times = dates[dates_key]["times"]
            for times_key in times.keys():
                if times[times_key]["votes"] > max_voted:
                    max_voted = times[times_key]["votes"]
                    most_voted_object["detail"] = {
                        "time": times[times_key],
                        "year": dates[dates_key]["year"],
                        "month": dates[dates_key]["month"],
                        "day": dates[dates_key]["day"],
                        "title": event["title"],
                        "description": event["description"],
                    }
        send_email(most_voted_object)
        return "Sent", 200
    else:
        return jsonify({"Detail": "Not found!"}), 404


@app.route("/users/signup", methods=["POST"])
def register_user():
    data = request.json
    if data not in users:
        users.append(data)
        return jsonify(data), 201
    return jsonify({"Detail": "Couldn't register user."}), 400


@app.route("/users/signin", methods=["POST"])
def login_user():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is not None and password is not None:
        user = list(filter(lambda user: user["email"] == email and user["password"] == password, users))
        if user:
            if email not in sessions:
                sessions.append(email)
                return jsonify(user), 200
            return jsonify({"Detail": "User already authenticated."}), 400
        return jsonify({"Detail": "Couldn't find any user with provided credentials."}), 404
    return jsonify({"Detail": "'email' and 'password' are required."}), 400


@app.route("/users/logout", methods=["POST"])
def logout_user():
    data = request.json
    email = data.get("email", None)
    if email:
        if email in sessions:
            sessions.remove(email)
            return jsonify({"Detail": "Logged out!"}), 200
        return jsonify({"Detail": "User is not authenticated."}), 400
    return jsonify({"Detail": "Email needs to be provided!"}), 400
