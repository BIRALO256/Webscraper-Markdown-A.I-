from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from service.config import config

sched = BlockingScheduler()
@sched.scheduled_job('cron', cron=config.scrape_cron)
def scheduled_scrape():
    requests.get("http://localhost:8000/scrape")

if __name__ == "__main__":
    sched.start()