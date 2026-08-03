from celery_app import app
import time

@app.task
def simulate_heavy_computation(x):
    print(f"[Worker] Starting heavy computation for x = {x}...")
    time.sleep(5)
    result = x * 2
    print(f"[Worker] Finished computation. Result = {result}")
    
    return result

#.delay() returns a AsyncResult output obj w/ fields id (.id) & metadata (.info)