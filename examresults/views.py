from examresults.models import ExamResultsActive
from django.db.models import Q
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView


class ExamsActiveView(TemplateView):
    template_name = "examresults/exams.html"
    model = ExamResultsActive
    context_object_name = "exams"
    queryset = ExamResultsActive.objects.order_by("exam_number")
    # template_name = "examresults/exams.html"  # Specify your own template name/location
    title_code = []
    title_description = []

    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        queryset = ExamResultsActive.objects.all()

        if query:
            print("Dispatch", query)
            if query.isnumeric():
                queryset = ExamResultsActive.objects.filter(
                    Q(exam_number=query) | Q(list_title_code=query)
                )
            else:

                queryset = ExamResultsActive.objects.filter(
                    list_title_desc__icontains=query
                )

        self.title_desc = [
            x["list_title_desc"] for x in queryset.values("list_title_desc").distinct()
        ]
        return super(ExamsActiveView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_desc"] = self.title_desc
        return context


class ExamJSON(BaseDatatableView):
    model = ExamResultsActive
    columns = [
        "exam_number",
        "list_title_code",
        "list_title_desc",
        "first_name",
        "middle_initial",
        "last_name",
        "adjust_final_average",
    ]
    order_columns = [
        "exam_number",
        "list_title_code",
        "list_title_desc",
        "first_name",
        "middle_initial",
        "last_name",
        "adjust_final_average",
    ]

    def get_initial_queryset(self, q=None):
        query = self.request.GET.get("q")
        print(self.request.GET)
        exams = ExamResultsActive.objects.none()
        if query:
            if query.isnumeric():
                exams = ExamResultsActive.objects.filter(
                    Q(exam_number=query) | Q(list_title_code=query)
                )
            else:
                exams = ExamResultsActive.objects.filter(
                    list_title_desc__icontains=query
                )
        return exams
