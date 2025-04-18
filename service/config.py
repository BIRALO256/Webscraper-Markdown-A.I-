# service/config.py
import os
from dotenv import load_dotenv

load_dotenv()                  # reads .env in the project root
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")