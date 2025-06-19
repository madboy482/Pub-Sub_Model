import json
import threading
from utils import subscribe, publish, check_redis_connection
import time

from configparser import ConfigParser

config = json.load(open('config.json'))
guest_responses = []

def handle_invitations():
    """Handle incoming invitations from hosts"""
    print("[Coordinator] 📨 Listening for invitations...")
    sub = subscribe(config['host_channel'])
    if not sub:
        print("[Coordinator] ❌ Failed to subscribe to host channel")
        return
        
    for msg in sub.listen():
        if msg['type'] == 'message':
            try:
                invitation = json.loads(msg['data'])
                print(f"[Coordinator] 📩 Received invitation: '{invitation['title']}' (ID: {invitation['event_id']})")
                print(f"[Coordinator] 📤 Forwarding to {len(config['guests'])} guests...")
                
                # Forward invitation to all guests
                for guest in config['guests']:
                    result = publish(guest, invitation)
                    if result:
                        print(f"[Coordinator] ✅ Sent to {guest}")
                    else:
                        print(f"[Coordinator] ❌ Failed to send to {guest}")
            except Exception as e:
                print(f"[Coordinator] ❌ Error processing invitation: {e}")

def handle_responses():
    """Handle responses from guests"""
    print("[Coordinator] 👥 Listening for guest responses...")
    sub = subscribe(config['guest_response_channel'])
    if not sub:
        print("[Coordinator] ❌ Failed to subscribe to response channel")
        return
        
    global guest_responses
    for msg in sub.listen():
        if msg['type'] == 'message':
            try:
                resp = json.loads(msg['data'])
                print(f"[Coordinator] 📨 Got response from {resp.get('guest', 'unknown')}: {resp}")
                
                # Only process invitation responses, ignore heartbeat messages
                if 'response' in resp and 'event_id' in resp:
                    guest_responses.append(resp)
                    print(f"[Coordinator] 📊 Responses collected: {len(guest_responses)}/{len(config['guests'])}")

                    # If all guests responded, send summary
                    if len(guest_responses) == len(config['guests']):
                        event_id = guest_responses[0]['event_id']  # All responses should have same event_id
                        summary = {
                            "event_id": event_id,
                            "total_guests": len(config['guests']),
                            "responses_received": len(guest_responses),
                            "confirmed": [r['guest'] for r in guest_responses if r['response'] == "Yes"],
                            "maybe": [r['guest'] for r in guest_responses if r['response'] == "Maybe"],
                            "declined": [r['guest'] for r in guest_responses if r['response'] == "No"],
                            "timestamp": time.time()
                        }
                        print(f"[Coordinator] 📋 Sending summary for event {event_id}")
                        result = publish(config['summary_channel'], summary)
                        if result:
                            print(f"[Coordinator] ✅ Summary sent successfully")
                        else:
                            print(f"[Coordinator] ❌ Failed to send summary")
                        guest_responses.clear()
                elif resp.get('type') == 'heartbeat':
                    # Just acknowledge heartbeat messages without processing them
                    pass
            except Exception as e:
                print(f"[Coordinator] ❌ Error processing response: {e}")

if __name__ == "__main__":
    print("\n🎯 EVENT COORDINATOR STARTING...")
    print("=" * 40)
    
    # Check Redis connection
    if not check_redis_connection():
        print("❌ Cannot connect to Redis. Please ensure Redis server is running.")
        exit(1)
    
    print("✅ Redis connection successful")
    print(f"📋 Configured for {len(config['guests'])} guests: {', '.join(config['guests'])}")
    print("🚀 Starting message handling threads...")
    
    # Start message handling threads
    invitation_thread = threading.Thread(target=handle_invitations, daemon=True)
    response_thread = threading.Thread(target=handle_responses, daemon=True)
    
    invitation_thread.start()
    response_thread.start()
    
    print("✅ Coordinator is ready!")
    print("📡 Listening for invitations and coordinating responses...")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Coordinator stopping...")
        print("✅ Coordinator stopped!")
