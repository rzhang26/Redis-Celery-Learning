'Storing Objects without JSON'
# import redis

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# user_data = {'name': 'Ray', 'role': 'director', 'login_count': 1}
# r.hset('user:1001', mapping=user_data)

# r.hincrby('user:1001', 'login_count', 4)

# profile = r.hmget('user:1001', ['name', 'login_count'])
# print(profile)

'Building a Shared FIFO Queue'
# import redis

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# r.rpush('task_queue', 'process_video_1')
# r.rpush('task_queue', 'process_video_2')
# r.rpush('task_queue', 'process_video_3')

# queue_name, task = r.blpop('task_queue', timeout=5)
# print(f'Processing: {task}...')

'Setting a Temporary Cache (Key Expiration)'
'v1'
# import redis

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# if r.exists('cached_api_response'):
#     data = r.get('cached_api_response')
#     print("Serving from cache:", data)
# else:
#     print("Cache miss! Fetching fresh data...")
#     data = 'heavy_data_string'
    
#     r.set(name='cached_api_response', value=data, ex=10)
'v2'
# import redis
# import time

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# r.set(name='cached_api_response', value='heavy_data_string',  ex=10)

# while True:
#     if r.exists('cached_api_response'):
#         data = r.get('cached_api_response')
#         print(data)
#         print('Serving from cache...')
#         time.sleep(3)
#     else:
#         print('No cache exists for this key...')
#         break

'Real-Time Broadcasts (Redis Pub/Sub)'
#runs in parallel with publisher.py
'v1'
# import redis
# import time

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# pubsub = r.pubsub()
# pubsub.subscribe('live_notifications')

# print('Waiting for messages...')
# for message in pubsub.listen():
#     if message['type'] == 'message':
#         print(f'Recieved alert: {message['data']}') 

'v2'
#more advanced version w/ allocation of sub-connection to background thread & time.sleep(5) for main thread
import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = r.pubsub()

# 1. Define a callback function to handle incoming messages automatically
def message_handler(message):
    print(f"Received alert in background: {message['data']}")

# 2. Map the channel directly to your callback function
pubsub.subscribe(**{'live_notifications': message_handler})

# 3. Start the background thread (daemon=True keeps it running in the background)
thread = pubsub.run_in_thread(sleep_time=0.01, daemon=True)
print('Background listener started. Waiting for messages...')

# 4. Your main thread is now completely free to do other tasks!
try:
    while True:
        print("Main thread is doing heavy work, sleeping for 5 seconds...")
        time.sleep(5)  # This sleep will NO LONGER block incoming messages!
except KeyboardInterrupt:
    # 5. Clean up the thread when you exit the script
    thread.stop()
    print("Stopped listener.")