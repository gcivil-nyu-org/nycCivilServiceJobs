from django.contrib import admin

from .models import ExamResultsTerminated, ExamResultsActive

admin.site.register(ExamResultsTerminated)
admin.site.register(ExamResultsActive)
