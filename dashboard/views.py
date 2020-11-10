from django.shortcuts import render, redirect, reverse
from django.views import View
from jobs.models import UserSavedJob, job_record
from examresults.models import ExamSchedule
from django_datatables_view.base_datatable_view import BaseDatatableView


# Create your views here.
class DashboardView(View):
    def get(self, request, *args, **kwargs):

        user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
        saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True))
        jobs = map(lambda x: x.job, user_saved_jobs)

        return render(
            request=request,
            template_name="dashboard/home.html",
            context={
                "user": request.user,
                "jobs": jobs,
                "saved_jobs_user": saved_jobs_user,
            },
        )


class SavedJobs(View):
    def get(self, request, *args, **kwargs):

        user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
        saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True))
        jobs = map(lambda x: x.job, user_saved_jobs)

        return render(
            request=request,
            template_name="dashboard/savedjobs.html",
            context={
                "user": request.user,
                "jobs": jobs,
                "saved_jobs_user": saved_jobs_user,
            },
        )


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard:dashboard"))

        total_jobs = job_record.objects.count()
        return render(
            request=request,
            template_name="index.html",
            context={"total_jobs": total_jobs},
        )


class ExamScheduleView(BaseDatatableView):
    model = ExamSchedule
    columns = [
        "exam_number",
        "exam_title_civil_service_title",
        "application_start_date",
        "application_end_date",
        "exam_type",
    ]
    order_columns = [
        "exam_number",
        "exam_title_civil_service_title",
        "application_start_date",
        "application_end_date",
        "exam_type",
    ]

    def get_context_data(self, *args, **kwargs):
        context = {
            "upcomingexams": ExamSchedule.objects.all(),
        }
        return context
