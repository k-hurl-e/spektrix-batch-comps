import os

event_id = os.getenv('EVENT_ID')
start_date = os.getenv('START_DATE')
performances = int(os.getenv('PERFORMANCES'))
extra_locks = int(os.getenv('EXTRA_LOCKS'))