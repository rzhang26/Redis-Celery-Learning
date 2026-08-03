'Offloading heavy HTTP requests'
# #works in tandem w/ route.py
# from celery import Celery
# import time

# worker = Celery('email_worker', broker='redis://localhost:6379/0')

# @worker.task
# def send_welcome_email(user_email, name):
#     time.sleep(4)
#     #some email sending logic & auth + authorization checks
#     print(f'Email has been successfully sent to {user_email} by {name}')
#     return True | None


'Tracking Task Progress and Fetching Results'
# from celery import Celery
# import time

# app = Celery('report_worker',
#              broker='redis://localhost:6379/0',
#              backend='redis://localhost:6379/0' #specify result_backend to fetch results later
#             )

# @app.task(bind=True) #bind=True to enable access to 'self' to update state
# def generate_heavy_report(self):
#     for i in range(1, 4):
#         #some heavy computation logic to generate the reports
#         time.sleep(2)
#         #self.state (ie. 'PROGRESS', 'COMPLETE', etc) can be consumed to create progress bar
#         self.update_state(state='PROGRESS', meta={'current': i, 'total': 3})

#     return {'download_url': 'https://storage.cdn'}


'Handling Network Flakes w/ Automatic Retries'
# from celery import Celery
# import requests

# worker = Celery(main='api_worker', broker='redis://localhost6379/0')

# @worker.task(bind=True, autoretry_for=(requests.exceptions.RequestException,), 
#              #trailing comma after RequestException to make arg a tuple
#              max_retries=3, 
#              default_retry_delay=5 
#             )
# def sync_crm_data(user_id, payloads):
#     #if third-party API errors out, Celery catches it and retries safely
#     response = requests.post(f'https://crm.com/{user_id}', json=payloads)
#     response.raise_for_status()

#     return 'Synced successfully.'

'Running Scheduled Cron Jobs (aka. Celery Beat)'
# from celery import Celery
# from celery.schedules import crontab

# app = Celery(main='cron_worker', broker='redis://localhost:6379/0')

# @app.task
# def clear_expired_sessions():
#     #some logic to delete_all() expired data in db or smth to clear db data
#     print('Database purged of expired user sessions.')

# #defining the recurring schedule
# app.conf.beat_schedule = {
#     'purge_every_night': {
#         'task': 'cron_worker.clear_expired_sessions',
#         'schedule': crontab(hour=0, minute=0) # executes at midnight
#     }
# }
# # (Note: To run this last example, you must start the scheduler daemon alongside your worker using celery -A cron_worker beat)

'Squential Chaining with Shared Data'
# from celery import Celery, chain
# import time

# app = Celery('workflow_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# @app.task
# def process_invoice(order_id):
#     return f'INV-{order_id}'

# @app.task
# def charge_credit_card(invoice_id, amount):
#     time.sleep(3)
#     print(f'Charing card for {invoice_id}: ${amount}')
#     return 'SUCCESS_CHARGE_TOKEN'

# @app.task
# def send_shipping_webhook(order_id):
#     time.sleep(3)
#     print(f'Notifying warehouse for order {order_id}')

# @app.task
# def handle_pipeline_failure(request, exc, traceback):
#     time.sleep(3)
#     print(f'Alert! Task {request} failed with error {exc}')

# order_id = 1111
# amount = 255.00

# order_flow = chain(
#     process_invoice.s(order_id),
#     charge_credit_card.s(amount),
#     send_shipping_webhook.si(order_id) #success_charge_token from prev output not taken in as arg here
# )

# order_flow.link_error(handle_pipeline_failure.s())
# order_flow.apply_async()

'High-Performance Chunking & Dynamic Chords'
# from celery import Celery, chord, group

# app = Celery('data_cruncher', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# @app.task
# def process_data_chunk(items_subset):
#     chunk_set = sum(x * 1.15 for x in items_subset)
#     return chunk_set

# @app.task
# def combine_and_save_metrics(all_chunk_sums):
#     final_metric = sum(all_chunk_sums)
#     print(f"All parallel jobs completed. Global sum adjusted: {final_metric}")
#     return final_metric

# large_dataset = list(range(1, 10001)) # 10,000 integers
# chunk_size = 1000

# chunk_generator = (
#     large_dataset[i:i + chunk_size] 
#     for i in range(0, len(large_dataset), chunk_size)
# )

# parallel_workers = group(process_data_chunk.s(batch) for batch in chunk_generator)
# pipeline = chord(parallel_workers)(combine_and_save_metrics.s())

#group syntax: group(task.s(input) for input in __list[input]__)
#chord syntax: chord(group)(callback) -> processes group tasks & passes their output into callback task(s)

'Deeply Nested Complex Trees'
from celery import Celery, group, chain

app = Celery(main='media_studio', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def extract_audio(video_file):
    return video_file.replace('.mp4', '.wav') #some complex logic/processes

@app.task
def translate_audio_to_text(audio_file, target_lang):
    return f'Transcribed text in {target_lang} for {audio_file}'

@app.task
def generate_srt_subtitles(transcription_text):
    return 'subtitles.srt'

video_source = 'movie_clip_101.mp4'

#the real 'meat' of the workflow: the pipelines
french_track = chain(
    translate_audio_to_text.s("FR"),
    generate_srt_subtitles.s()
)
spanish_track = chain(
    translate_audio_to_text.s("ES"), 
    generate_srt_subtitles.s()
)

localization_pipeline = chain(
    extract_audio.s(video_source),
    group(
        french_track,
        spanish_track
    )
)

localization_pipeline.apply_async() 
#apply_async() just makes it works asynchronously (very abstract but very convenient)