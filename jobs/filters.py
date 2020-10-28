from .models import job_record
import django_filters

business_titles = job_record.objects.all().values_list('business_title').distinct()
agencies = job_record.objects.all().values_list('agency').distinct()


class JobFilter(django_filters.FilterSet):

    class Meta:
        model = job_record
        fields = [
            "business_title",
            "agency",
            "posting_date",
            "career_level",
            "full_time_part_time_indicator",
        ]
