# Event Management API (Flask CRUD)

A simple RESTful API built with Python and Flask for managing events. It supports creating, reading, updating, and deleting events, using an in-memory list of `Event` objects to simulate a database.

## Setup

```bash
pip install flask
python app.py
```

The server runs at `http://localhost:5000`.

## Routes

| Method | Route           | Description                  | Success code |
|--------|-----------------|------------------------------|--------------|
| GET    | `/`             | Welcome message              | 200          |
| GET    | `/events`       | List all events              | 200          |
| POST   | `/events`       | Create a new event           | 201          |
| PATCH  | `/events/<id>`  | Update an event's title      | 200          |
| DELETE | `/events/<id>`  | Delete an event              | 204          |

Errors:
- `400 Bad Request` if `title` is missing from the JSON body
- `404 Not Found` if no event matches the given ID

## Example requests and responses

### GET /
```json
{ "message": "Welcome to the Event Management API" }
```

### GET /events
```json
[
  { "id": 1, "title": "Tech Meetup" },
  { "id": 2, "title": "Python Workshop" }
]
```

### POST /events
Request body:
```json
{ "title": "Hackathon" }
```
Response (201):
```json
{ "id": 3, "title": "Hackathon" }
```

### PATCH /events/1
Request body:
```json
{ "title": "Hackathon 2025" }
```
Response (200):
```json
{ "id": 1, "title": "Hackathon 2025" }
```

### DELETE /events/2
Response: `204 No Content` (empty body)

### Error example (PATCH /events/99)
Response (404):
```json
{ "error": "Event not found" }
```

## Notes
- Data is stored in memory, so it resets every time the server restarts.
- A `find_event_by_id` helper avoids repeating lookup logic across routes.
- The code is structured so a real database can replace the in-memory list later.