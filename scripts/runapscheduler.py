# runapscheduler.py
import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
import sys
import exam_notify as en  # noqa: E402


def my_job():
    print("Job Execution")
    en.notify_exams()
    pass


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


scheduler = BlockingScheduler(settings.SCHEDULER_CONFIG)
scheduler.add_job(
    my_job,
    "interval",
    minutes=1,
    id="notify",
    replace_existing=True,
)
scheduler.add_job(
    delete_old_job_executions,
    trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
    id="delete_old_job_executions",
    max_instances=1,
    replace_existing=True,
)

scheduler.start()
