from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

event_id = os.getenv('EVENT_ID')
start_date = os.getenv('START_DATE')
performances = int(os.getenv('PERFORMANCES'))
extra_locks = int(os.getenv('EXTRA_LOCKS'))
