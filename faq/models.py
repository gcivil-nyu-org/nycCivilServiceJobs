from django.db import models

# Create your models here.


class faq(models.Model):
    faq_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Frequently Asked Questions"
