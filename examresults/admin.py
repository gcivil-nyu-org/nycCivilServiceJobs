from django.contrib import admin

from .models import (
    ExamResultsTerminated,
    ExamResultsActive,
    ExamSchedule,
    CivilServicesTitle,
)


class ExamActiveAdmin(admin.ModelAdmin):
    list_display = (
        "exam_number",
        "list_number",
        "first_name",
        "last_name",
        "middle_initial",
        "adjust_final_average",
        "list_title_code",
        "list_title_desc",
        "group_number",
        "list_agency_code_promo",
        "list_agency_code_promo_desc",
        "list_div_code_promo",
        "published_date",
        "established_date",
        "anniversary_date",
        "extension_date",
        "veteran_credit",
        "parent_legacy_credit",
        "sibling_legacy_credit",
        "residency_credit",
    )


class ExamTerminatedAdmin(admin.ModelAdmin):
    list_display = ("exam_number", "list_title_code", "list_title_desc")


class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "exam_number",
        "exam_title_civil_service_title",
        "application_start_date",
        "application_end_date",
        "exam_type",
    )


class CivilServicesTitleAdmin(admin.ModelAdmin):
    list_display = ("title_code", "title_description")


admin.site.register(ExamResultsTerminated, ExamTerminatedAdmin)
admin.site.register(ExamResultsActive, ExamActiveAdmin)
admin.site.register(ExamSchedule, ExamScheduleAdmin)
admin.site.register(CivilServicesTitle, CivilServicesTitleAdmin)
