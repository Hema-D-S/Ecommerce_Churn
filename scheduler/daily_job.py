# scheduler/daily_job.py

from apscheduler.schedulers.blocking import BlockingScheduler
from run_daily_job import run_daily_job

# Initialize the scheduler
scheduler = BlockingScheduler()

# Define the scheduled job
@scheduler.scheduled_job('interval', hour=9, minute=0)  # Change to hours=24 for daily runs
def scheduled_job():
    print("⏰ Running daily job...")
    run_daily_job()

if __name__ == "__main__":
    print("🚀 Starting scheduler...")
    run_daily_job()  # Optional: run once immediately at startup
    scheduler.start()
