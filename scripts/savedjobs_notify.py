import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

from jobs.models import job_record, UserSavedJob
from django.core import mail
from django.template.loader import render_to_string
import datetime


def send_email(to, subject, content):
    mail.send_mail(subject, content, None, [to], html_message=content)


def notify_jobs():
    queryset = UserSavedJob.objects.filter(
        job__post_until__gte=datetime.date.today(),
        job__post_until__lte=datetime.date.today() + datetime.timedelta(days=2),
    )

    users = queryset.values_list("user", flat=True).distinct()
    email = ""
    for user in users:
        user_sub = queryset.filter(user=user)

        job_list = []

        for obj in user_sub:
            job_id = obj.job.job_id

            job_list.extend(
                job_record.objects.filter(
                    job_id=job_id,
                )
            )

        if job_list:
            obj = user_sub[0]
            email = obj.user.email
            message = render_to_string(
                "dashboard/savedjobs_notify.html",
                {"first_name": obj.user.first_name, "jobs": job_list},
            )
            send_email(email, "Upcoming Jobs Notification", message)


notify_jobs()
