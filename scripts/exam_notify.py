import sys, os, django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

from dashboard.models import ExamResultsSubscription, ExamSubscription
from examresults.models import ExamResultsActive, ExamSchedule
from django.core import mail
from register.models import User
from django.template.loader import render_to_string
import datetime


def send_email(to, subject, content):

    mail.send_mail(subject, content, None, [to], html_message=content)


def notify_exams():
    queryset = ExamSubscription.objects.filter(is_notified=False)
    exams = {}
    users = queryset.values_list("user", flat=True).distinct()
    email = ""
    for user in users:
        user_sub = queryset.filter(user=user)

        exam_list = []
        for obj in user_sub:
            title = obj.civil_service_title.title_description
            if title not in exams:
                exams[title] = ExamSchedule.objects.filter(
                    exam_title_civil_service_title=title,
                    application_start_date__lte=datetime.date.today()
                    + datetime.timedelta(days=2),
                    application_start_date__gte=datetime.date.today(),
                )
            if exams[title]:
                exam_list.extend(exams[title])
        message = render_to_string(
            "dashboard/upcomingexam_notify.html",
            {"first_name": obj.user.first_name, "title": title, "exams": exam_list},
        )

        if user_sub:
            email = user_sub[0].user.email
            send_email(email, "Upcoming Exam Notification", message)
        for obj in user_sub:
            obj.is_notified = True
            obj.save()


# def notify_results():
#     queryset = ExamResultsSubscription.objects.filter(is_notified=False)
#     for obj in queryset:
#         if ExamActiveResults.filter(list_title_code=obj.civil_service_title.title_code).exists():
#             message = render_to_string(
#                 "dashboard/examresults_notify.html",
#                 {
#                     "first_name": obj.user.first_name,
#                     "Civil Service Title": obj.civil_service_title.title_description,
#
#                 },
#             )
#             send_email(obj.user.email,"Exam Results Notification",message)
#             obj.is_notified=True
#             obj.save()

notify_exams()
