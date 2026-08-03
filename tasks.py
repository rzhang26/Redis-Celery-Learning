import time

from celery_app import celery_app

#tasks placed in seperate file from celery_app (consideration by scaling)

@celery_app.task(bind=True)
def simulate_heavy_computation(self, x: int):
    if x < 0:
        raise ValueError('Input {x} for x can not be negative.')
    
    print(f"[Worker] Starting heavy computation for x = {x}...")
    time.sleep(30)

    result = x * 2
    print(f"[Worker] Finished computation. Result = {result}.")

    return result