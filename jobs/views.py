from django.views.generic import TemplateView, ListView, View
from .models import job_record, UserSavedJob
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string


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

    agencies = []
    career_level = []
    cs_titles = []
    salary_ranges = []

    def dispatch(self, request, *args, **kwargs):
        self.agencies = [
            x["agency"] for x in job_record.objects.values("agency").distinct()
        ]
        self.career_level = [
            x["career_level"]
            for x in job_record.objects.values("career_level").distinct()
            if x["career_level"]
        ]

        self.cs_titles = [
            x["civil_service_title"]
            for x in job_record.objects.values("civil_service_title").distinct()
        ]
        self.salary_ranges = [[0, 10000], [10000, 20000], [20000, 45000], [450000, "+"]]
        return super(SearchResultsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agencies"] = self.agencies
        context["career_level"] = self.career_level
        context["cs_titles"] = self.cs_titles
        if self.request.user.is_authenticated:
            context["saved_jobs_user"] = list(
                UserSavedJob.objects.filter(user=self.request.user).values_list(
                    "job", flat=True
                )
            )
        else:
            context["saved_jobs_user"] = None
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query is None:
            query = ""
        # agency_query = self.request.GET.get("agency_query", None)
        # posting_type_query = self.request.GET.get("posting_type_query", None)

        object_list = job_record.objects.filter(
            Q(agency__icontains=query)
            | Q(business_title__icontains=query)
            | Q(civil_service_title__icontains=query)
        ).order_by("-posting_date")

        self.query_set = object_list
        return object_list

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            # print("AJAX" ,self.request.POST,self.request.GET)
            query = request.POST.get("query")
            jobs = job_record.objects.filter(
                Q(agency__icontains=query)
                | Q(business_title__icontains=query)
                | Q(civil_service_title__icontains=query)
            )
            form_filters = {}

            posting_type = request.POST.get("posting_type")
            date = request.POST.get("date")
            agency = request.POST.get("agency")
            career_level = request.POST.get("career_level")
            salary_range = request.POST.get("salary_range")
            cs_title_index = request.POST.get("cs_title")
            # print("Career Level: ",salary_range)

            sort_order = request.POST.get("sort_order")
            asc = request.POST.get("asc")
            fp = request.POST.get("fp")
            if posting_type:
                form_filters["posting_type"] = posting_type
            if date:
                form_filters["posting_date__gte"] = date
            if agency and len(self.agencies):
                form_filters["agency"] = self.agencies[int(agency)]
            if fp:
                form_filters["full_time_part_time_indicator"] = fp
            if career_level and len(self.career_level):
                form_filters["career_level"] = self.career_level[int(career_level)]
            if salary_range:
                form_filters["salary_range_from__gte"] = int(salary_range)
            if cs_title_index and len(self.cs_titles):
                form_filters["civil_service_title"] = self.cs_titles[
                    int(cs_title_index)
                ]

            # print(posting_type,date,self.agencies[int(agency)])
            jobs = jobs.filter(**form_filters)

            sort_field = ""
            if sort_order:
                if sort_order == "sort-posting":
                    sort_field = "posting_date"
                elif sort_order == "sort-salary":
                    sort_field = "salary_range_from"
                if asc == "false":
                    sort_field = "-" + sort_field
                jobs = jobs.order_by(sort_field)

            context = {"jobs": jobs}

            if self.request.user.is_authenticated:
                context["saved_jobs_user"] = list(
                    UserSavedJob.objects.filter(user=self.request.user).values_list(
                        "job", flat=True
                    )
                )
            else:
                context["saved_jobs_user"] = None

            # csrf_token = request.POST.get("csrfmiddlewaretoken")
            # context["csrf_token"] = csrf_token
            # print(context)
            data = {
                "rendered_table": render_to_string(
                    "jobs/table_content.html", context=context, request=request
                )
            }
            # data = serializers.serialize('json', data)
            return JsonResponse(data, safe=False)


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
