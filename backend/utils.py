import json
import redis

# Load configuration
config = json.load(open('config.json'))
redis_config = config.get('redis', {})

# Create Redis connection with configuration
r = redis.Redis(
    host=redis_config.get('host', 'localhost'),
    port=redis_config.get('port', 6379),
    decode_responses=redis_config.get('decode_responses', True)
)

def publish(channel, message):
    """Publish a message to a Redis channel"""
    try:
        result = r.publish(channel, json.dumps(message))
        return result
    except Exception as e:
        print(f"Error publishing to {channel}: {e}")
        return None

def subscribe(channel):
    """Subscribe to a Redis channel"""
    try:
        pubsub = r.pubsub()
        pubsub.subscribe(channel)
        return pubsub
    except Exception as e:
        print(f"Error subscribing to {channel}: {e}")
        return None

def check_redis_connection():
    """Check if Redis server is accessible"""
    try:
        r.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False
