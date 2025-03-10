from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Body
from models.email import EmailSchema
from services.email_sender import send_email_with_attachment
router = APIRouter()

@router.post("/send-email/")
async def send_email_route(
    background_task: BackgroundTasks,
    email_data: EmailSchema = Body(...),
):
    # file_content = await file.read() if file else None
    # file_name = file.filename if file else None

    background_task.add_task(
        send_email_with_attachment,
        email_data.recipient,
        email_data.subject,
        email_data.body,
        # file_content,
        # file_name
    )

    return {"message":"Email is being sent"}