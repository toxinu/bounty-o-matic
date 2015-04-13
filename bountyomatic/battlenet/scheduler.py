import time
import schedule
from carotte import Client


def run_task(task_name, *args, **kwargs):
    client = Client()
    client.run_task(task_name, *args, **kwargs)

schedule.every(20).hours.do(run_task, 'refresh_characters')

while True:
    schedule.run_pending()
    time.sleep(1)
