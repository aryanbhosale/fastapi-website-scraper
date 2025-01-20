import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
