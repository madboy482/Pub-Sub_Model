from utils import publish, subscribe
import json
import uuid
import time

config = json.load(open('config.json'))

def create_event():
    """Create an event with user input or use default"""
    print("\n=== Event Host Console ===")
    print("Create a new event invitation:")
    
    title = input("Event Title (or press Enter for default): ").strip()
    if not title:
        title = "Pizza Party @ My Place"
    
    event_time = input("Event Time (or press Enter for default): ").strip()
    if not event_time:
        event_time = "8:00 PM tonight"
    
    event = {
        "event_id": str(uuid.uuid4()),
        "title": title,
        "time": event_time,
        "created_at": time.time()
    }
    
    return event

def main():
    event = create_event()
    
    print(f"\n[Host] 📤 Sending invitation for: '{event['title']}'")
    print(f"[Host] Event ID: {event['event_id']}")
    print(f"[Host] Time: {event['time']}")
    print(f"[Host] Waiting for responses from {len(config['guests'])} guests...")
    
    # Send invitation to coordinator
    publish(config['host_channel'], event)

    # Wait for summary from coordinator
    sub = subscribe(config['summary_channel'])
    for msg in sub.listen():
        if msg['type'] == 'message':
            summary = json.loads(msg['data'])
            
            # Check if this summary is for our event
            if summary.get('event_id') == event['event_id']:
                print("\n" + "="*50)
                print("🎊 FINAL GUEST LIST SUMMARY 🎊")
                print("="*50)
                print(f"Event: {event['title']}")
                print(f"Time: {event['time']}")
                print(f"Event ID: {summary['event_id']}")
                print(f"\nTotal Invited: {summary['total_guests']}")
                print(f"Responses Received: {summary['responses_received']}")
                
                print(f"\n✅ CONFIRMED ({len(summary['confirmed'])} guests):")
                for guest in summary['confirmed']:
                    print(f"   • {guest}")
                
                print(f"\n🤔 MAYBE ({len(summary['maybe'])} guests):")
                for guest in summary['maybe']:
                    print(f"   • {guest}")
                
                print(f"\n❌ DECLINED ({len(summary['declined'])} guests):")
                for guest in summary['declined']:
                    print(f"   • {guest}")
                
                print("\n" + "="*50)
                print("Event planning complete! 🎉")
                break

if __name__ == "__main__":
    main()
