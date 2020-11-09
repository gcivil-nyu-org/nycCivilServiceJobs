from django.views import generic
from examresults.models import ExamResultsActive
from django.db.models import Q


class ExamsActiveView(generic.ListView):
    model = ExamResultsActive
    context_object_name = "exams"
    queryset = ExamResultsActive.objects.order_by("exam_number")
    template_name = "examresults/exams.html"  # Specify your own template name/location
    title_code = []
    title_description = []

    def dispatch(self, request, *args, **kwargs):
        self.title_code = [
            x["list_title_code"]
            for x in ExamResultsActive.objects.values("list_title_code").distinct()
        ]
        self.title_desc = [
            x["list_title_desc"]
            for x in ExamResultsActive.objects.values("list_title_desc").distinct()
        ]
        return super(ExamsActiveView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_code"] = self.title_code
        context["title_desc"] = self.title_desc
        print(len(self.title_code))
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", None)
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
        return None
