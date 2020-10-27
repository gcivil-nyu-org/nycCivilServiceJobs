from django.db import models

# Create your models here.


class job_record(models.Model):
    job_id = models.IntegerField()
    agency = models.CharField(max_length=200, null=True, blank=True)
    posting_type = models.CharField(max_length=50, null=True, blank=True)
    num_positions = models.IntegerField(null=True, blank=True)
    business_title = models.CharField(max_length=200, null=True, blank=True)
    civil_service_title = models.CharField(max_length=200, null=True, blank=True)
    title_classification = models.CharField(max_length=200, null=True, blank=True)
    title_code_no = models.CharField(max_length=50, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    job_category = models.CharField(max_length=200, null=True, blank=True)
    full_time_part_time_indicator = models.CharField(
        max_length=50, null=True, blank=True
    )  # Full-time/Part-time
    career_level = models.CharField(max_length=200, null=True, blank=True)
    salary_range_from = models.FloatField(null=True, blank=True)
    salary_range_to = models.FloatField(null=True, blank=True)
    salary_frequency = models.CharField(max_length=50, null=True, blank=True)
    work_location = models.TextField(null=True, blank=True)
    division_work_unit = models.CharField(max_length=200, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    minimum_qual_requirements = models.TextField(null=True, blank=True)
    preferred_skills = models.TextField(null=True, blank=True)
    additional_information = models.TextField(null=True, blank=True)
    to_apply = models.TextField(null=True, blank=True)
    hours_shift = models.TextField(null=True, blank=True)
    work_location_1 = models.TextField(null=True, blank=True)
    recruitment_contact = models.CharField(max_length=200, null=True, blank=True)
    residency_requirement = models.TextField(null=True, blank=True)
    posting_date = models.DateTimeField(null=True, blank=True)
    post_until = models.DateField(null=True, blank=True)
    posting_updated = models.DateTimeField(null=True, blank=True)
    process_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.job_id)

    class Meta:
        verbose_name_plural = "Job Records"
