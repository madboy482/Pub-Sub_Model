import sys
import random
import time
from utils import subscribe, publish
import json

config = json.load(open('config.json'))

guest_name = sys.argv[1] if len(sys.argv) > 1 else "guest1"

# Simulated guest preferences for more realistic responses
guest_preferences = {
    "guest1": {"likelihood": 0.8, "response_time": 2},  # Usually says yes, responds quickly
    "guest2": {"likelihood": 0.5, "response_time": 4},  # Uncertain, takes time to decide
    "guest3": {"likelihood": 0.3, "response_time": 3},  # Usually declines, moderate response time
}

def simulate_decision_making(invitation_title):
    """Simulate realistic guest decision making"""
    preference = guest_preferences.get(guest_name, {"likelihood": 0.6, "response_time": 3})
    
    # Simulate thinking time
    thinking_time = preference["response_time"] + random.uniform(0, 2)
    print(f"[{guest_name}] Thinking about invitation: '{invitation_title}'...")
    time.sleep(thinking_time)
    
    # Make decision based on likelihood
    rand_val = random.random()
    if rand_val < preference["likelihood"] * 0.7:  # 70% of likelihood for "Yes"
        return "Yes"
    elif rand_val < preference["likelihood"]:  # Remaining likelihood for "Maybe"
        return "Maybe"
    else:
        return "No"

def main():
    print(f"[{guest_name}] Starting up and waiting for invitations...")
    sub = subscribe(guest_name)
    
    for msg in sub.listen():
        if msg['type'] == 'message':
            try:
                invitation = json.loads(msg['data'])
                print(f"[{guest_name}] 📨 Received invitation: '{invitation['title']}' at {invitation['time']}")

                # Simulate decision making process
                response = simulate_decision_making(invitation['title'])
                
                # Add some personality to the responses
                reactions = {
                    "Yes": "🎉 Excited to attend!",
                    "Maybe": "🤔 Will try to make it...",
                    "No": "😔 Sorry, can't make it"
                }
                
                print(f"[{guest_name}] {reactions[response]} Responding: {response}")

                # Send response back to coordinator
                response_data = {
                    "guest": guest_name,
                    "response": response,
                    "event_id": invitation['event_id'],
                    "timestamp": time.time()
                }
                
                publish(config['guest_response_channel'], response_data)
                
            except Exception as e:
                print(f"[{guest_name}] Error processing invitation: {e}")

if __name__ == "__main__":
    main()
