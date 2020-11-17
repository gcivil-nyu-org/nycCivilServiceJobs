# runapscheduler.py
import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution

from django_apscheduler.jobstores import register_job
import sys
import exam_notify as en  # noqa: E402

scheduler = BlockingScheduler(settings.SCHEDULER_CONFIG)


def my_job():
    print("Exam Notifications")
    en.notify_exams()
    en.notify_results()
    pass


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


scheduler.add_job(
    my_job,
    "cron",
    day_of_week="mon-fri",
    hour=0,
    minute=5,
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
