from fastapi import APIRouter, BackgroundTasks, Body, Request,  HTTPException
from models.email import EmailSchema
from services.email_sender import send_email_with_attachment
from core.oauth import oauth
from core.config import mail_settings
import secrets
import json

router = APIRouter(prefix="/gmail")

# --------------------------
# Helper Functions
# --------------------------
def validate_state(store_state: str, received_state: str) -> bool:
    """Securely compare state parameters"""
    return secrets.compare_digest(store_state,received_state)

def store_toke_in_session(request: Request, token: dict):
    """Handle token storage consistently"""
    request.session.update({
        "access_token": token.get("access_token"),
        "refresh_token":token.get("refresh_token"),
        "expires_at":token["expires_at"]
    })


# --------------------------
# Route handlers
# --------------------------

@router.post("/send-email")
async def send_email_route(
    background_task: BackgroundTasks,
    email_data: EmailSchema = Body(...),
):
    background_task.add_task(
        send_email_with_attachment,
        email_data.recipient,
        email_data.subject,
        email_data.body,
        # file_content,
        # file_name
    )

    return {"message":"Email is being sent"}


@router.post("/authorize")
async def authorize_hubspot(request: Request):
    """
    Redirect the user Gmail OAuth2 authorization endpoint
    """
    state = secrets.token_urlsafe(32) #<- Generate a secure random state
    request.session["oauth_state"] = state
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri=mail_settings.REDIRECT_URI,
        state=state
    )


@router.get("/callback")
async def auth_callback(request: Request, state: str = None):
    # Error Handling
    if error := request.query_params.get("error"): # walrus operator
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {error}"
        )

    # state validate
    stored_state = request.session.get("oauth_state")
    if validate_state(stored_state , state):
        raise HTTPException(
            status_code=400,
            detail="Invalid state parameter"
        )
    
    # Get Access token using authorization
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, details=str(e))
    
    # Store tokens
    store_toke_in_session(request)

    return json.dumps(request)
