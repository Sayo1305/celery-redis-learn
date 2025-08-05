from fastapi import APIRouter
from pydantic import BaseModel
from app.task import generate_pdf
from celery.result import AsyncResult
from app.celery_app import app
from fastapi import HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os


router = APIRouter()

class PDFRequest(BaseModel):
    email: str
    name: str
    desc: str
    password: str

@router.get("/")
def read_root():
    return {"message": "Hello, FastAPI! working"}

@router.post("/generate_pdf")
def create_pdf(request: PDFRequest):
    task = generate_pdf.delay(request.dict())
    return {"status": "ok", "message": "PDF generation started" , "task" : task.id}



@router.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=app)

    return {
        "task_id": task_id,
        "status": task_result.status,  # PENDING, STARTED, SUCCESS, FAILURE, etc.
        "result": str(task_result.result) if task_result.ready() else None
    }


@router.get("/download/{task_id}")
def get_download(task_id: str, background_tasks: BackgroundTasks):
    task_result = AsyncResult(task_id, app=app)
    
    if not task_result.ready():
        raise HTTPException(status_code=202, detail="Task is still processing")
    
    if task_result.failed():
        raise HTTPException(status_code=500, detail="Task failed")
    
    output_path = str(task_result.result)
    
    # Check if file exists
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Schedule file deletion in background after response is sent
    background_tasks.add_task(os.remove, output_path)

    # Extract filename
    filename = os.path.basename(output_path)

    return FileResponse(
        path=output_path,
        filename=filename,
        media_type='application/octet-stream',
        background=background_tasks
    )