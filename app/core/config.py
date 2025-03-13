import os 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST","redis")
    REDIS_PORT: int = os.getenv("REDIS_PORT",6379)
    REDIS_DB: int = 0

class MailSettings:
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = os.getenv("SMTP_PORT", 587)
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL")

    CLIENT_ID: str =  os.getenv("GMAIL_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("GMAIL_CLIENT_SECRET")

    REDIRECT_URI: str = "http://localhost:8000/gmail/callback"
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GMAIL_API_URL = "https://www.googleapis.com/gmail/v1/"

redis_settings = RedisSettings()
mail_settings = MailSettings()