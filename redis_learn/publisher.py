import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.publish('live_notifications', 'System rebooting in 5 seconds.')