# Redis: In-memory Data Store

import redis

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Set a key-value pair
r.set("name", "Alice")

# Get the value
print(r.get("name"))
