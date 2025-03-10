from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailSchema(BaseModel):
    recipient: str
    subject: str 
    body: str