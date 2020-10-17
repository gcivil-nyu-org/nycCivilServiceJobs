from django.db import models

# Create your models here.

class ExamResultsActive(models.Model):
    exam_number = models.IntegerField(null=True)
    list_number = models.FloatField(null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_initial  = models.CharField(max_length=30, blank=True,null=True)
    adjust_final_average = models.FloatField(null=True)
    list_title_code = models.IntegerField(null=True)
    list_title_desc = models.CharField(max_length=250, blank=True,null=True)
    group_number = models.IntegerField(null=True)
    list_agency_code_promo = models.IntegerField(null=True)
    list_agency_code_promo_desc = models.CharField(max_length=250, blank=True,null=True)
    list_div_code_promo = models.CharField(max_length=30, blank=True,null=True)
    published_date = models.DateTimeField(null=True)
    established_date  = models.DateTimeField(null=True)
    anniversary_date  = models.DateTimeField(null=True)
    extention_date = models.DateTimeField(null=True)
    veteran_credit = models.CharField(max_length=100, blank=True,null=True)
    parent_legacy_credit = models.CharField(max_length=100, blank=True,null=True)
    sibling_legacy_credit = models.CharField(max_length=100, blank=True,null=True)
    residency_credit = models.CharField(max_length=100, blank=True,null=True)

class ExamResultsTerminated(models.Model):
    exam_number = models.IntegerField(null=True)
    list_title_code = models.IntegerField(null=True)
    list_title_desc = models.CharField(max_length=250, blank=True, null=True)

def __int__(self):
    return self.exam_number