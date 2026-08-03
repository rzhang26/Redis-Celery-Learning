from fastapi import FastAPI, status
from typing import Optional, Any, List
from pydantic import BaseModel, Field
from celery.result import AsyncResult
from celery.exceptions import TimeoutError

from celery_app import celery_app
from tasks import simulate_heavy_computation

app = FastAPI(title='FastAPI & Celery Task Queue API')

class ExecutionRequest(BaseModel):
    x: int = Field(..., description="Integer payload for worker", example=10)

class TaskResponse(BaseModel):
    job_id: str
    status: str
    message: str

@app.post('/execute-code', response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def execute_code(payload: ExecutionRequest):
    task = simulate_heavy_computation.delay(payload.x)

    return {
        'job_id': str(task.id),
        'status': 'COMPLETE',
        'message': 'Task submitted successfully.'
    }

@app.get('/results/{job_id}')
def submit(job_id: str, wait_timeout: float = 0.0):
    task_result = AsyncResult(job_id, app=celery_app)

    if wait_timeout > 0:
        try:
            result = task_result.get(timeout=wait_timeout)
            return {
                'job_id': job_id,
                'status': task_result.status,
                'result': result
            }
        except TimeoutError:
            pass
        except Exception as exc:
            return {
                'job_id': job_id,
                'status': 'FAILURE',
                'error': str(exc)
            }

    if task_result.state == 'PENDING':
        return {
            'job_id': job_id,
            'status': 'PENDING',
            'message': 'Task is queued or in progress'
        }   
    elif task_result.state == 'SUCCESS':
            return {
                'job_id': job_id,
                'status': 'SUCCESS',
                'message': task_result.result
            }   
    elif task_result.state == 'FAILURE':
        return {
            'job_id': job_id,
            'status': 'PENDING',
            'message': str(task_result.result)
        }   
    else:
        return {
            'job_id': job_id,
            'status': task_result.state
        }
    