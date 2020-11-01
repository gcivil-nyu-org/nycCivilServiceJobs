from django.views.generic import TemplateView, ListView, View
from .models import job_record, UserSavedJob
from django.db.models import Q
from django.http import JsonResponse


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all().order_by("posting_date").reverse()[:10],
        }
        if self.request.user.is_authenticated:
            context["saved_jobs_user"] = list(
                UserSavedJob.objects.filter(user=self.request.user).values_list(
                    "job", flat=True
                )
            )
        else:
            context["saved_jobs_user"] = None

        return context


class SearchResultsView(ListView):
    model = job_record
    template_name = "jobs/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        object_list = job_record.objects.filter(
            Q(agency__icontains=query)
            | Q(business_title__icontains=query)
            | Q(civil_service_title__icontains=query)
        )
        return object_list


class SaveJobsView(View):
    def post(self, request, *args, **kwargs):

        # print(request.POST['jobs_pk_id'])
        if self.request.method == "POST":
            job_record_pk = self.kwargs["pk"]
            job = job_record.objects.get(pk=job_record_pk)
            user = request.user
            response_data = {"job_id": job_record_pk}
            if user.is_authenticated:
                already_saved = UserSavedJob.objects.filter(user=user, job=job)
                if already_saved.count() == 0:
                    save_job = UserSavedJob(user=user, job=job)
                    save_job.save()
                    response_data["response_data"] = "Job Saved"
                else:
                    already_saved.delete()
                    response_data["response_data"] = "Job Unsaved"

                # print("inside post")
                return JsonResponse(response_data, status=200)

            else:
                # messages.error(self.request, "Invalid username or password.")
                # print ('inside post else')
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)

            return JsonResponse({"error": ""}, status=400)
