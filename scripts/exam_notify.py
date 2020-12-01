import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

from dashboard.models import ExamResultsSubscription, ExamSubscription
from examresults.models import ExamResultsActive, ExamSchedule
from django.core import mail
from django.template.loader import render_to_string
import datetime
from django.shortcuts import reverse
from django.contrib.sites.models import Site


def send_email(to, subject, content):

    mail.send_mail(subject, content, None, [to], html_message=content)


def notify_exams():
    queryset = ExamSubscription.objects.filter(is_notified=False)
    exams = {}
    users = queryset.values_list("user", flat=True).distinct()
    email = ""
    current_site = Site.objects.get_current()
    dashboard_url = "".join(
        ["http://", current_site.domain, "/signin/?next=/dashboard"]
    )

    for user in users:
        user_sub = queryset.filter(user=user)

        exam_list = []

        for obj in user_sub:
            title = obj.civil_service_title.title_description
            if title not in exams:
                exams[title] = ExamSchedule.objects.filter(
                    exam_title_civil_service_title__iexact=title,
                    application_start_date=datetime.date.today(),
                )
            if exams[title]:
                exam_list.extend(exams[title])

                obj.is_notified = True
                obj.save()

            earlynotif = ExamSchedule.objects.filter(
                exam_title_civil_service_title__iexact=title,
                application_start_date=datetime.date.today()
                + datetime.timedelta(days=5),
            )
            if earlynotif:
                exam_list.extend(earlynotif)

        if exam_list:
            obj = user_sub[0]
            email = obj.user.email
            message = render_to_string(
                "dashboard/upcomingexam_notify.html",
                {
                    "first_name": obj.user.first_name,
                    "exams": exam_list,
                    "url": dashboard_url,
                },
            )
            send_email(email, "Upcoming Exams Notification", message)


def notify_results():
    queryset = ExamResultsSubscription.objects.filter(is_notified=False)
    users = queryset.values_list("user", flat=True).distinct()

    current_site = Site.objects.get_current()
    results_url = "".join(
        ["http://", current_site.domain, reverse("examresults:exams")]
    )

    for user in users:
        examresults = []
        user_exam = queryset.filter(user=user)
        for obj in user_exam:
            results = ExamResultsActive.objects.filter(
                exam_number=obj.exam_number,
                # first_name__iexact=obj.user.first_name,
                # last_name__iexact=obj.user.last_name,
            ).first()
            if results:
                examresults.append(results)
        if examresults:
            obj = user_exam[0]
            message = render_to_string(
                "dashboard/examresults_notify.html",
                {
                    "first_name": obj.user.first_name,
                    "results": examresults,
                    "url": results_url,
                },
            )
            send_email(obj.user.email, "Exam Results Notification", message)
            for obj in user_exam:
                obj.is_notified = True
                obj.save()


notify_exams()
notify_results()
