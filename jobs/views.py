from django.views.generic import TemplateView, ListView
from .models import job_record
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string


class JobsView(TemplateView):
    template_name = "jobs/jobs.html"

    def get_context_data(self, *args, **kwargs):
        context = {
            "jobs": job_record.objects.all().order_by("posting_date").reverse()[:10],
        }
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


class SearchFilterView(ListView):
    model = job_record
    template_name = "jobs/search_filter.html"
    agencies = [x["agency"] for x in job_record.objects.values("agency").distinct()]
    career_level = [
        x["career_level"] for x in job_record.objects.values("career_level").distinct()
    ]
    print(career_level)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agencies"] = self.agencies
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
        )
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
            sort_order = request.POST.get("sort_order")
            asc = request.POST.get("asc")
            fp = request.POST.get("fp")
            print(sort_order, asc)
            if posting_type:
                form_filters["posting_type"] = posting_type
            if date:
                form_filters["posting_date__gte"] = date
            if agency and len(self.agencies):
                form_filters["agency"] = self.agencies[int(agency)]
            if fp:
                form_filters["full_time_part_time_indicator"] = fp
            # print(posting_type,date,self.agencies[int(agency)])
            jobs = jobs.filter(**form_filters)

            sort_field = ""
            if sort_order:
                if sort_order == "sort-posting":
                    sort_field = "posting_date"

                if asc == "false":
                    sort_field = "-" + sort_field
                print("Order By: ", sort_field)
                jobs = jobs.order_by(sort_field)

            context = {"jobs": jobs}
            data = {
                "rendered_table": render_to_string(
                    "jobs/table_content.html", context=context
                )
            }
            # data = serializers.serialize('json', data)
            return JsonResponse(data, safe=False)
