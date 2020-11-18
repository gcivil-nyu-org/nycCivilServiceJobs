from django.shortcuts import render, redirect, reverse
from django.views import View
from jobs.models import UserSavedJob, job_record
from examresults.models import ExamSchedule
import datetime
from django.http.response import JsonResponse
from examresults.models import CivilServicesTitle

# import json
from dashboard.models import ExamSubscription, ExamResultsSubscription


# Create your views here.
class DashboardView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
            saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True))
            jobs = map(lambda x: x.job, user_saved_jobs)
            exam_schedule = ExamSchedule.objects.filter(
                application_end_date__gte=datetime.date.today()
            )
            user_subscribed_exams_count = ExamSubscription.objects.filter(
                user=self.request.user
            ).count()
            user_subscribed_exam_results_count = ExamResultsSubscription.objects.filter(
                user=self.request.user
            ).count()
            user_subscriptions_count = (
                user_subscribed_exams_count + user_subscribed_exam_results_count
            )
            return render(
                request=request,
                template_name="dashboard/home.html",
                context={
                    "user": request.user,
                    "jobs": jobs,
                    "saved_jobs_user": saved_jobs_user,
                    "exam_schedule": exam_schedule,
                    "user_subscriptions_count": user_subscriptions_count,
                },
            )
        else:
            return redirect(reverse("index"))


class SavedJobs(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

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
        else:
            return redirect(reverse("index"))


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


class SubscriptionView(View):  # pragma: no cover
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            civil_services_title_all = CivilServicesTitle.objects.all()
            user_subscribed_exams = ExamSubscription.objects.filter(
                user=self.request.user
            )
            user_subscribed_exam_results = ExamResultsSubscription.objects.filter(
                user=self.request.user
            )

            return render(
                request,
                "dashboard/subscription.html",
                context={
                    "user": request.user,
                    "civil_services_title_all": civil_services_title_all,
                    "user_subscribed_exams": user_subscribed_exams,
                    "user_subscribed_exam_results": user_subscribed_exam_results,
                },
            )
        else:
            return redirect(reverse("signin:signin"))


class SaveCivilServiceTitleView(View):  # pragma: no cover
    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            cst = request.POST.get("civilservicetitleid")
            # cstname = request.POST.get("civilservicetitle")
            # print(cstname)
            user = request.user
            response_data = {
                "count_before": ExamSubscription.objects.filter(user=user).count()
            }
            if user.is_authenticated:
                civilServiceTitle = CivilServicesTitle.objects.get(pk=cst)
                already_saved = ExamSubscription.objects.filter(
                    user=user, civil_service_title=civilServiceTitle
                )
                if already_saved.count() == 0:
                    save_civilServiceTitle = ExamSubscription(
                        user=user,
                        civil_service_title=civilServiceTitle,
                    )
                    save_civilServiceTitle.save()
                    response_data["response_data"] = "CIVIL_SERVICE_TITLE_SAVED"
                    response_data[
                        "subscribed_title"
                    ] = civilServiceTitle.title_description
                    response_data["subscribed_id"] = ExamSubscription.objects.get(
                        user=user, civil_service_title=civilServiceTitle
                    ).id
                else:
                    response_data[
                        "response_data"
                    ] = "CIVIL_SERVICE_TITLE_ALREADY_PRESENT"

                return JsonResponse(response_data, status=200)

            else:
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


class SaveExamNumberView(View):  # pragma: no cover
    def post(self, request, *args, **kwargs):

        if self.request.method == "POST":
            examNo = request.POST.get("examno")
            # print(examNo)
            user = request.user
            response_data = {
                "count_before": ExamResultsSubscription.objects.filter(
                    user=user
                ).count()
            }
            if user.is_authenticated:

                already_saved = ExamResultsSubscription.objects.filter(
                    user=user, exam_number=examNo
                )
                if already_saved.count() == 0:
                    save_examNo = ExamResultsSubscription(
                        user=user,
                        exam_number=examNo,
                    )
                    save_examNo.save()
                    response_data["response_data"] = "EXAM_SAVED"
                    response_data["subscribed_exam_num"] = examNo
                    response_data[
                        "subscribed_exam_id"
                    ] = ExamResultsSubscription.objects.get(
                        user=user, exam_number=examNo
                    ).id
                else:
                    response_data["response_data"] = "EXAM_ALREADY_PRESENT"

                return JsonResponse(response_data, status=200)

            else:
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


class ExamResultsDeleteView(View):  # pragma: no cover
    def post(self, request, *args, **kwargs):

        if self.request.method == "POST":
            examNo = request.POST.get("examno")
            user = request.user
            response_data = {
                "count_before": ExamResultsSubscription.objects.filter(
                    user=user
                ).count()
            }
            if user.is_authenticated:

                already_saved = ExamResultsSubscription.objects.get(id=examNo)

                if already_saved:
                    already_saved.delete()
                    response_data["response_data"] = "EXAM_SUBSCRIBED_DELETED"
                    response_data["exam_deleted_id"] = examNo

                else:
                    response_data["response_data"] = "EXAM_TITLE_NOT_PRESENT"

                return JsonResponse(response_data, status=200)

            else:
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


class CivilServiceTitleDeleteView(View):  # pragma: no cover
    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            cst = request.POST.get("civilservicetitleid")
            user = request.user
            response_data = {
                "count_before": ExamSubscription.objects.filter(user=user).count()
            }
            if user.is_authenticated:
                already_saved = ExamSubscription.objects.get(id=cst)
                if already_saved:
                    already_saved.delete()
                    response_data["response_data"] = "CIVIL_SERVICE_TITLE_DELETED"
                    response_data["cst_deleted_id"] = cst

                else:
                    response_data["response_data"] = "CIVIL_SERVICE_TITLE_NOT_PRESENT"

                return JsonResponse(response_data, status=200)

            else:
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)
