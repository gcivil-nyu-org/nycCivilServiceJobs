import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

from jobs.models import job_record, UserSavedJob
from django.core import mail
from django.shortcuts import reverse
from django.template.loader import render_to_string
import datetime
from django.contrib.sites.models import Site


def send_email(to, subject, content):
    mail.send_mail(subject, content, None, [to], html_message=content)


def notify_jobs():
    queryset = UserSavedJob.objects.filter(
        job__post_until__gte=datetime.date.today(),
        job__post_until__lte=datetime.date.today() + datetime.timedelta(days=2),
    )

    users = queryset.values_list("user", flat=True).distinct()
    email = ""

    current_site = Site.objects.get_current()
    savedjobs_url = "".join(
        ["http://", current_site.domain, reverse("dashboard:savedjobs")]
    )

    for user in users:
        user_sub = queryset.filter(user=user)

        job_list = []

        for obj in user_sub:
            job_list.append(obj.job)

        if job_list:
            obj = user_sub[0]
            email = obj.user.email
            message = render_to_string(
                "dashboard/savedjobs_notify.html",
                {
                    "first_name": obj.user.first_name,
                    "jobs": job_list,
                    "url": savedjobs_url,
                },
            )
            send_email(email, "Saved Jobs Notification", message)


notify_jobs()
