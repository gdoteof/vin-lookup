import os
from apscheduler.schedulers.blocking import BlockingScheduler
from app.telly_api import vin_service
from app import create_app
from datetime import datetime

sched = BlockingScheduler()


#@sched.scheduled_job('cron', hour='07', minute='00')
@sched.scheduled_job('cron', hour='05', minute='30')
def update_cars():
    print("Starting scraper")
    try:
        scraping_enabled = os.getenv("ENABLE_SCRAPING", 'True')
        if scraping_enabled != 'True':
            print("scraping not enabled")
        else:
            batch_size = int(os.getenv("SCRAPER_BATCH_SIZE", 1000))
            print(f"Scraping with batch size {batch_size}")
            config_name = os.getenv('FLASK_CONFIG')
            app = create_app(config_name)
            app.app_context().push()
            vin_service.get_next_batch(batch_size)
    except Exception as e:
        print(f"Error scraping: {e}")

#@sched.scheduled_job('cron', hour='21', minute='10')
@sched.scheduled_job('cron', hour='23')
def update_missing_cars():
    try:
        start = int(os.getenv("MISSING_START", 74812 ))
        limit = int(os.getenv("MISSING_LIMIT", 1000))
        print(f'searching missing from {start} limit {limit}')
        config_name = os.getenv('FLASK_CONFIG')
        app = create_app(config_name)
        app.app_context().push()
        vin_service.find_missing_cars(start, limit)
    except Exception as e:
        print(f"Error scraping: {e}")

sched.start()
