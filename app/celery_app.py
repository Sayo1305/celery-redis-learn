from celery import Celery
from dotenv import load_dotenv
import os
load_dotenv()
BROKER_URL = os.getenv("BROKER_URL")
BACKEND_URL = os.getenv("BACKEND_URL")

app = Celery(
      "my_tasks" , 
      broker=BROKER_URL , 
      backend=BACKEND_URL,
)