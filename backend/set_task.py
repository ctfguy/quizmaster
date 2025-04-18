from celery.schedules import crontab
from app.tasks import celery, send_daily_reminders, generate_monthly_report

# WORK IN PROGRESS

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=0),
        send_daily_reminders.s(),
        name='send daily reminders'
    )
    
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=6, minute=0),
        generate_monthly_report.s(),
        name='generate monthly reports'
    )

if __name__ == '__main__':
    print("Scheduled tasks set up:")
    print("1. Daily reminders: 7:00 PM every day")
    print("2. Monthly reports: 6:00 AM on the 1st of every month")