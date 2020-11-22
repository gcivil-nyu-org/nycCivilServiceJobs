# Register your models here.
from django.contrib import admin
from dashboard.models import ExamSubscription, ExamResultsSubscription

admin.site.register(ExamSubscription)
admin.site.register(ExamResultsSubscription)
