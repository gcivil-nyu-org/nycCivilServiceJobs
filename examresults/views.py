from django.shortcuts import render
from django.views import generic
from examresults.models import *

class ExamsActiveView(generic.ListView):
    model = ExamResultsActive
    context_object_name = 'exams'
    paginate_by = 50
    queryset = ExamResultsActive.objects.order_by("exam_number")[:400]
    template_name = 'examresults/exams.html'  # Specify your own template name/location
