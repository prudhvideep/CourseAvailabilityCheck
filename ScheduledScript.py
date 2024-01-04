import schedule
import time
from subprocess import call

def job():
    print("Running your_script.py...")
    call(["python", "MainScript.py"])

# Schedule the job every 10 minutes
schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
