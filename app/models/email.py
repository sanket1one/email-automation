from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailSchema(BaseModel):
    recipient: str
    subject: str 
    body: str

class TokenData(BaseModel):
    access_token: str 
    refresh_toke: Optional[str] = None 
    expire_in: int 
    token_type: str 

class AccountInfo(BaseModel):
    portalId: int 
    portalName: Optional[str] = None

class GmailOAuthResponse(BaseModel):
    token_data: TokenData
    account_info: AccountInfo