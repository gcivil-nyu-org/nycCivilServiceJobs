from django.db import models


class ExamResultsActive(models.Model):
    exam_number = models.IntegerField(null=True)
    list_number = models.FloatField(null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=30, blank=True, null=True)
    adjust_final_average = models.FloatField(null=True)
    list_title_code = models.IntegerField(null=True)
    list_title_desc = models.CharField(max_length=250, blank=True, null=True)
    group_number = models.IntegerField(null=True)
    list_agency_code_promo = models.IntegerField(null=True)
    list_agency_code_promo_desc = models.CharField(
        max_length=250, blank=True, null=True
    )
    list_div_code_promo = models.CharField(max_length=30, blank=True, null=True)
    published_date = models.DateTimeField(null=True)
    established_date = models.DateTimeField(null=True, blank=True)
    anniversary_date = models.DateTimeField(null=True, blank=True)
    extension_date = models.DateTimeField(null=True, blank=True)
    veteran_credit = models.CharField(max_length=100, blank=True, null=True)
    parent_legacy_credit = models.CharField(max_length=100, blank=True, null=True)
    sibling_legacy_credit = models.CharField(max_length=100, blank=True, null=True)
    residency_credit = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Exam Results(Active)"


class ExamResultsTerminated(models.Model):
    exam_number = models.IntegerField(null=True)
    list_title_code = models.IntegerField(null=True)
    list_title_desc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Exam Results(Terminated)"


class ExamSchedule(models.Model):
    exam_number = models.IntegerField(null=True)
    exam_title_civil_service_title = models.CharField(
        max_length=250, blank=True, null=True
    )
    application_start_date = models.DateField(null=True, blank=True)
    application_end_date = models.DateField(null=True, blank=True)
    exam_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Upcoming Exam Schedule"

    def __int__(self):
        return self.exam_number


class CivilServicesTitle(models.Model):
    title_code = models.CharField(max_length=200, null=True, blank=True)
    title_description = models.CharField(max_length=200, null=True, blank=True)
    # standard_hours = models.FloatField(null=True, blank=True)
    # assignment_level = models.FloatField(null=True, blank=True)
    # union_code = models.IntegerField(null=True, blank=True)
    # union_description = models.TextField(null=True, blank=True)
    # bargaining_unit_short_name = models.CharField(max_length=200,null=True, blank=True)
    # minimum_salary_rate = models.FloatField(null=True, blank=True)
    # maximum_salary_rate = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Civil Services Title"

    def __str__(self):
        return self.title_code
