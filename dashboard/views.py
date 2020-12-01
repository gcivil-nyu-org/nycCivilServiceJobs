from django.shortcuts import render, redirect, reverse
from django.views import View
from jobs.models import UserSavedJob, job_record
from examresults.models import ExamSchedule
import datetime
from django.http.response import JsonResponse
from examresults.models import CivilServicesTitle, ExamResultsActive
from django.db.models import Q


# import json
from dashboard.models import ExamSubscription, ExamResultsSubscription
from signin.models import UsersCivilServiceTitle


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

        total_jobs = job_record.objects.filter(
            Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)
        ).count()
        return render(
            request=request,
            template_name="index.html",
            context={"total_jobs": total_jobs},
        )


class SubscriptionView(View):
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


class SaveCivilServiceTitleView(View):
    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            cst = request.POST.get("civilservicetitleid")
            # cstname = request.POST.get("civilservicetitle")
            # print(cstname)
            user = request.user
            response_data = {}

            if user.is_authenticated:
                response_data = {
                    "count_before": ExamSubscription.objects.filter(user=user).count()
                }
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


class SaveExamNumberView(View):
    def post(self, request, *args, **kwargs):

        if self.request.method == "POST":
            examNo = request.POST.get("examno")
            # print(examNo)
            user = request.user
            response_data = {}
            if user.is_authenticated:
                response_data = {
                    "count_before": ExamResultsSubscription.objects.filter(
                        user=user
                    ).count()
                }

                already_saved = ExamResultsSubscription.objects.filter(
                    user=user, exam_number=examNo
                )

                already_released = ExamResultsActive.objects.filter(
                    exam_number=examNo,
                )

                if already_released.count() > 0:
                    response_data["subscribed_exam_num"] = examNo
                    response_data["response_data"] = "EXAM_ALREADY_RELEASED"

                elif already_saved.count() == 0:
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


class ExamResultsDeleteView(View):
    def post(self, request, *args, **kwargs):

        if self.request.method == "POST":
            examNo = request.POST.get("examno")
            user = request.user
            response_data = {}
            if user.is_authenticated:
                response_data = {
                    "count_before": ExamResultsSubscription.objects.filter(
                        user=user
                    ).count()
                }

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


class CivilServiceTitleDeleteView(View):
    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            cst = request.POST.get("civilservicetitleid")
            user = request.user
            response_data = {}
            if user.is_authenticated:
                response_data = {
                    "count_before": ExamSubscription.objects.filter(user=user).count()
                }
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


class RecommendedJobs(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            user_saved_jobs = UserSavedJob.objects.filter(user=self.request.user)
            saved_jobs_user = list(user_saved_jobs.values_list("job", flat=True))
            jobs = self.recommendjobs(request)

            return render(
                request=request,
                template_name="dashboard/recommendedjobs.html",
                context={
                    "user": request.user,
                    "jobs": jobs,
                    "saved_jobs_user": saved_jobs_user,
                },
            )
        else:
            return redirect(reverse("index"))

    def recommendjobs(self, request):
        if request.user.is_authenticated:

            user_civil_services_title = UsersCivilServiceTitle.objects.filter(
                user=self.request.user
            )

            user_curr_civil_services_title = list(
                user_civil_services_title.filter(is_interested=False).values_list(
                    "civil_service_title__title_description", flat=True
                )
            )
            # print(user_curr_civil_services_title)
            hold_cst = set()
            for title in user_curr_civil_services_title:
                hold_job = (
                    job_record.objects.filter(
                        Q(civil_service_title__iexact=title)
                        & (Q(post_until__gte=datetime.date.today()))
                    )
                    .distinct()
                    .order_by("-posting_date")[:10]
                )
            for job in hold_job:
                hold_cst.add(job.civil_service_title)

            hold_cst = list(hold_cst)
            # print(hold_cst)

            user_interested_civil_services_title = list(
                user_civil_services_title.filter(is_interested=True).values_list(
                    "civil_service_title__title_description", flat=True
                )
            )
            interested_cst = set()
            for int_title in user_interested_civil_services_title:
                int_job = job_record.objects.filter(
                    Q(civil_service_title__iexact=int_title)
                    & (Q(post_until__gte=datetime.date.today()))
                ).order_by("-posting_date")[:10]

            for job in int_job:
                interested_cst.add(job.civil_service_title)

            interested_cst = list(interested_cst)
            # print(interested_cst)

            user_saved_civil_service = list(
                UserSavedJob.objects.filter(user=self.request.user)
                .values_list("job__civil_service_title", flat=True)
                .distinct()
            )
            # print(user_saved_civil_service)

            new_saved_cst = []
            for job in user_saved_civil_service:
                if (job not in hold_cst) and (job not in interested_cst):
                    new_saved_cst.append(job)
            # print(new_saved_cst)

            new_saved_job = set()
            for save_job in new_saved_cst:
                saved_cst = job_record.objects.filter(
                    Q(civil_service_title__iexact=save_job)
                    & (Q(post_until__gte=datetime.date.today()))
                ).order_by("-posting_date")[:10]
            # print(saved_cst)

            for job in saved_cst:
                new_saved_job.add(job.civil_service_title)
            new_saved_job = list(new_saved_job)
            # print(new_saved_job)

            final_jobs = hold_job | int_job | saved_cst

            # print(final_jobs.count())
            if final_jobs.count() > 10:
                final_jobs = final_jobs.order_by("-posting_date")[:10]
                return final_jobs

            else:
                return final_jobs
