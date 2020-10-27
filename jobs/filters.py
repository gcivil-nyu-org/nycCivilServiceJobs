from .models import *
import django_filters
from django.db.models import Q

business_titles = job_record.objects.all().values_list('business_title').distinct()
agencies = job_record.objects.all().values_list('agency').distinct()


class JobFilter(django_filters.FilterSet):
    # business_title = django_filters.ChoiceFilter(
    #     field_name="business_title", lookup_expr="icontains", label="Job Title"
    # )
    # agency = django_filters.ChoiceFilter(
    #     field_name="agency", lookup_expr="icontains", label="Agency"
    # )
    # posting_date = django_filters.DateFromToRangeFilter(
    #     field_name="posting_date", label="Posted (Between)"
    # )
    # career_level = django_filters.CharFilter(
    #     field_name="career_level", lookup_expr="icontains", label="Career Level"
    # )
    # full_time_part_time_indicator = django_filters.CharFilter(
    #     field_name="full_time_part_time_indicator", lookup_expr="icontains", label="Full-time or Part-time"
    # )

    class Meta:
        model = job_record
        fields = [
            "business_title",
            "agency",
            "posting_date",
            "career_level",
            "full_time_part_time_indicator",
        ]
