import redis

# Basic connection
r = redis.Redis(host='localhost', port=6379, db=0)

# With URL
r = redis.from_url("redis://localhost:6379/0")

# With password & decode responses
r = redis.Redis(
    host='localhost',
    port=6379,
    password='yourpassword',
    decode_responses=True  # Returns str instead of bytes
)

# Test connection
r.ping()  # True
