import time
import schedule
from .carotte import refresh_characters

schedule.every(20).hours.do(refresh_characters)

while True:
    schedule.run_pending()
    time.sleep(1)
