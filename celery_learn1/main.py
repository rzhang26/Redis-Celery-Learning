'Offloading heavy HTTP requests'
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from typing import Optional, List, Any

# # from tasks import worker, send_welcome_email
# #have db & configs

# @asynccontextmanager
# async def lifespan():
#     #database empty edge case check
#     #session open, close
#     pass 

# app = FastAPI(title='main_app', root_path='', lifespan=lifespan)

# # @app.post()
# # async def send_emails(user_emails: List[str], names: List[str]):
# #     #manual input validation checks or just specify pydantic/sqlmodel validation during typing
# #     for i in range(len(user_emails)):
# #         send_welcome_email.delay(user_emails[i], names[i])
# #         print(f'Response sent to user {user_emails[i]} by {names[i]}')

# #     return None

'Tracking Task Progress and Fetching Results'
from tasks import generate_heavy_report
from celery.result import AsyncResult

#all of these can go inside enpoints

#useful fields / objs
task = generate_heavy_report.delay() #.delay() makes task compatible w/ asynchronous ops
task_id = task.id

#check status & metadata
result = AsyncResult(task_id)
print(f'Task State: {result.state}')
print(f'Task Meta: {result.info}')

#block and get final result when ready
final_data = result.get(timeout=10)
print(f'Report Complete! URL is {final_data['download_url']}')


