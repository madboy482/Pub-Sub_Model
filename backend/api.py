from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import publish, subscribe
import json
import uuid
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
config = json.load(open('config.json'))
summaries = {}
active_events = {}

def listen_for_summary(event_id):
    """Listen for summary responses from coordinator"""
    sub = subscribe(config['summary_channel'])
    for msg in sub.listen():
        if msg['type'] == 'message':
            try:
                summary = json.loads(msg['data'])
                if summary.get('event_id') == event_id:
                    summaries[event_id] = summary
                    if event_id in active_events:
                        active_events[event_id]['status'] = 'completed'
                    print(f"[API] Received summary for event {event_id}")
                    break
            except Exception as e:
                print(f"[API] Error processing summary: {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Event Planner API",
        "version": "1.0",
        "endpoints": {
            "send_invite": "POST /send-invite",
            "get_summary": "GET /get-summary/<event_id>",
            "get_events": "GET /events"
        }
    })

@app.route("/send-invite", methods=["POST"])
def send_invite():
    try:
        data = request.json
        
        if not data or not data.get("title"):
            return jsonify({"error": "Event title is required"}), 400
        
        event_id = str(uuid.uuid4())
        event = {
            "event_id": event_id,
            "title": data.get("title"),
            "time": data.get("time", "Time TBD"),
            "created_at": time.time()
        }
        
        # Store active event info
        active_events[event_id] = {
            "event": event,
            "status": "pending",
            "created_at": time.time()
        }
        
        # Publish invitation to coordinator
        publish(config['host_channel'], event)
        
        # Start listening for summary in background
        threading.Thread(target=listen_for_summary, args=(event_id,), daemon=True).start()
        
        print(f"[API] Created event: {event['title']} (ID: {event_id})")
        
        return jsonify({
            "message": "Invitation sent successfully",
            "event_id": event_id,
            "event": event,
            "guests_invited": len(config['guests'])
        })
        
    except Exception as e:
        print(f"[API] Error sending invite: {e}")
        return jsonify({"error": "Failed to send invitation"}), 500

@app.route("/get-summary/<event_id>", methods=["GET"])
def get_summary(event_id):
    try:
        if event_id in summaries:
            return jsonify(summaries[event_id])
        
        # Check if event exists
        if event_id in active_events:
            return jsonify({
                "message": "Summary not ready yet. Guests are still responding...",
                "status": "pending",
                "event": active_events[event_id]["event"]
            }), 202
        
        return jsonify({"error": "Event not found"}), 404
        
    except Exception as e:
        print(f"[API] Error getting summary: {e}")
        return jsonify({"error": "Failed to retrieve summary"}), 500

@app.route("/events", methods=["GET"])
def get_events():
    """Get all active events and their status"""
    try:
        events_list = []
        for event_id, event_data in active_events.items():
            event_info = {
                "event_id": event_id,
                "title": event_data["event"]["title"],
                "time": event_data["event"]["time"],
                "status": event_data["status"],
                "created_at": event_data["created_at"]
            }
            
            # Add summary if available
            if event_id in summaries:
                event_info["summary"] = summaries[event_id]
            
            events_list.append(event_info)
        
        return jsonify({
            "events": events_list,
            "total_events": len(events_list)
        })
        
    except Exception as e:
        print(f"[API] Error getting events: {e}")
        return jsonify({"error": "Failed to retrieve events"}), 500

if __name__ == "__main__":
    print("🚀 Starting Event Planner API Server...")
    print("📡 Endpoints available:")
    print("   POST /send-invite - Send event invitation")
    print("   GET /get-summary/<event_id> - Get event summary")
    print("   GET /events - List all events")
    app.run(debug=True, host='0.0.0.0', port=5000)
