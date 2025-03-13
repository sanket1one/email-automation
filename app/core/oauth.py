from authlib.integrations.starlette_client import OAuth
from core.config import mail_settings

oauth = OAuth()

def setup_oauth():
    oauth.register(
        name='google',
        client_id = mail_settings.CLIENT_ID,
        client_secret = mail_settings.CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile https://www.googleapis.com/auth/gmail.send',
            'prompt': 'consent',    # <- Force consent screen
            'access_type': 'offline' # <- Get refresh toke
        }
    )
    return oauth