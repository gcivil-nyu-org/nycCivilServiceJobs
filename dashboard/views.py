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

        user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
        saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True))
        jobs = map(lambda x: x.job, user_saved_jobs)
        exam_schedule = ExamSchedule.objects.filter(
            application_end_date__gte=datetime.date.today()
        )
        return render(
            request=request,
            template_name="dashboard/home.html",
            context={
                "user": request.user,
                "jobs": jobs,
                "saved_jobs_user": saved_jobs_user,
                "exam_schedule": exam_schedule,
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


class SubscriptionView(View):  # pragma: no cover
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            civil_services_title_all = CivilServicesTitle.objects.all()

            return render(
                request,
                "dashboard/subscription.html",
                context={
                    "user": request.user,
                    "civil_services_title_all": civil_services_title_all,
                },
            )
        else:
            return redirect(reverse("signin:signin"))


class SaveCivilServiceTitleView(View):  # pragma: no cover
    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            cst = request.POST.get("civilservicetitleid")
            cstname = request.POST.get("civilservicetitle")
            print(cstname)
            user = request.user

            response_data = {
                "count_before": ExamSubscription.objects.filter(user=user).count()
            }
            print(response_data)
            if user.is_authenticated:
                civilServiceTitle = CivilServicesTitle.objects.get(pk=cst)
                print(civilServiceTitle)

                #  already_saved = list(
                #     ExamSubscription.objects.filter(user=user).values_list(
                #         "civil_service_title", flat=True
                #     )
                # )
                already_saved = ExamSubscription.objects.filter(
                    user=user, civil_service_title=civilServiceTitle
                )
                # seen = set(already_saved)
                if not already_saved:
                    save_civilServiceTitle = ExamSubscription(
                        user=user,
                        civil_service_title=civilServiceTitle,
                    )
                    save_civilServiceTitle.save()
                    response_data["response_data"] = "CIVIL_SERVICE_TITLE_SAVED"
                    response_data[
                        "subscribed_title"
                    ] = civilServiceTitle.title_description
                else:
                    response_data[
                        "response_data"
                    ] = "CIVIL_SERVICE_TITLE_ALREADY_PRESENT"

                # already_saved = list(seen)
                # print(already_saved)

                # print(response_data["subscribed_titles"])

                # response_data["subsribed_titles"] = json.dumps(civilServiceTitle)

                return JsonResponse(response_data, status=200)

            else:
                # messages.error(self.request, "Invalid username or password.")
                # print ('inside post else')
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


class SaveExamNumberView(View):
    # pragma: no cover
    def post(self, request, *args, **kwargs):

        if self.request.method == "POST":
            examNo = request.POST.get("examno")
            print(examNo)
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
                else:
                    response_data["response_data"] = "Exam_Already_Saved"

                # user_exams_subscribed = ExamResultsSubscription.objects.filter(
                #     user=user
                # )

                # response_data["user_exams_subscribed"] = json.dumps(
                #     user_exams_subscribed
                # )

                response_data = {
                    "response_data": "EXAM_SAVED",
                    "subscribed_result": examNo,
                }
                return JsonResponse(response_data, status=200)

            else:
                # messages.error(self.request, "Invalid username or password.")
                # print ('inside post else')
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)


class ExamResultsDeleteView(View):
    def get(self, request):
        id1 = request.GET.get("examid", None)
        ExamResultsSubscription.objects.get(exam_number=id1).delete()
        data = {"deleted": True}
        return JsonResponse(data)


class CivilServiceTitleDeleteView(View):
    def get(self, request):
        cst1 = request.GET.get("civilservicetitle", None)
        ExamSubscription.objects.get(exam_number=cst1).delete()
        data = {"deleted": True}
        return JsonResponse(data)
