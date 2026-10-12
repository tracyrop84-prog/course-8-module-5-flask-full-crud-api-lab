from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database" (resets every time the server restarts)
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Helper: find an event by its ID (avoids repeating the same loop in every route)
def find_event_by_id(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


# GET / - Welcome message
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


# GET /events - Return all events as a JSON array
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # silent=True returns None instead of raising an error if the body isn't valid JSON
    data = request.get_json(silent=True)

    # Input validation: title is required
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    # Generate the next ID (max existing ID + 1, or 1 if the list is empty)
    new_id = max((event.id for event in events), default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # 201 Created for a successful POST
    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    # 204 No Content: success, with no response body
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)