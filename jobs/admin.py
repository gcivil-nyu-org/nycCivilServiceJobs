from django.contrib import admin
from .models import job_record


class JobsAdmin(admin.ModelAdmin):
    list_display = (
        "job_id",
        "agency",
        "posting_type",
        "num_positions",
        "business_title",
        "civil_service_title",
        "title_classification",
        "title_code_no",
        "level",
        "job_category",
        "full_time_part_time_indicator",
        "career_level",
        "salary_range_from",
        "salary_range_to",
        "salary_frequency",
        "work_location",
        "division_work_unit",
        # 'job_description',
        # 'minimum_qual_requirements',
        # 'preferred_skills',
        # 'additional_information',
        # 'to_apply',
        "hours_shift",
        "work_location_1",
        "recruitment_contact",
        # 'residency_requirement',
        "posting_date",
        "post_until",
        "posting_updated",
        "process_date",
    )

    list_filter = ["posting_date"]
    search_fields = ["job_id"]


# Register your models here.
admin.site.register(job_record, JobsAdmin)
