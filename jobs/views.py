from django.views.generic import TemplateView, ListView, View
from .models import job_record, UserSavedJob
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
import datetime


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all()
            .filter(
                Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)
            )
            .order_by("-posting_date")[:10],
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
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get("q") or request.POST.get("query")
        queryset = job_record.objects.all()
        if query:
            queryset = job_record.objects.filter(
                (
                    Q(agency__icontains=query)
                    | Q(business_title__icontains=query)
                    | Q(civil_service_title__icontains=query)
                ),
                (Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)),
            )

        self.agencies = [x["agency"] for x in queryset.values("agency").distinct()]
        self.career_level = [
            x["career_level"]
            for x in queryset.values("career_level").distinct()
            if x["career_level"]
        ]

        self.cs_titles = [
            x["civil_service_title"]
            for x in queryset.values("civil_service_title").distinct()
        ]
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
            (
                Q(agency__icontains=query)
                | Q(business_title__icontains=query)
                | Q(civil_service_title__icontains=query)
            ),
            (Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)),
        ).order_by("-posting_date")

        self.query_set = object_list
        return object_list

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            query = request.POST.get("query")
            jobs = job_record.objects.filter(
                (
                    Q(agency__icontains=query)
                    | Q(business_title__icontains=query)
                    | Q(civil_service_title__icontains=query)
                ),
                (Q(post_until__gte=datetime.date.today()) | Q(post_until__isnull=True)),
            ).order_by("-posting_date")

            form_filters = {}

            posting_type = request.POST.get("posting_type")
            date = request.POST.get("date")
            agency = request.POST.get("agency")
            career_level = request.POST.get("career_level")
            salary_range = request.POST.get("salary_range")
            cs_title_index = request.POST.get("cs_title")
            fp = request.POST.get("fp")
            sort_order = request.POST.get("sort_order")
            asc = request.POST.get("asc")

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

            jobs = jobs.filter(**form_filters)

            sort_field = "-posting_date"
            if sort_order:
                if sort_order == "sort-posting":
                    sort_field = "posting_date"
                elif sort_order == "sort-salary":
                    sort_field = "salary_range_from"
                if asc == "false":
                    sort_field = "-" + sort_field
            jobs = jobs.order_by(sort_field)
            context = {"jobs": jobs}
            paginator = Paginator(jobs, 20)
            context["paginator"] = paginator
            context["is_paginated"] = True
            page = request.POST.get("page")
            page_number = 1
            if page and int(page) != -1:
                page_number = int(page)

            context["jobs"] = paginator.page(page_number)

            if self.request.user.is_authenticated:
                context["saved_jobs_user"] = list(
                    UserSavedJob.objects.filter(user=self.request.user).values_list(
                        "job", flat=True
                    )
                )
            else:
                context["saved_jobs_user"] = None

            data = {
                "rendered_table": render_to_string(
                    "jobs/table_content.html", context=context, request=request
                ),
                "count": jobs.count(),
            }

            return JsonResponse(data, safe=False)


class SaveJobsView(View):
    def post(self, request, *args, **kwargs):

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

                return JsonResponse(response_data, status=200)

            else:
                # messages.error(self.request, "Invalid username or password.")
                response_data["response_data"] = "User not authenticated"
                return JsonResponse(response_data, status=200)
