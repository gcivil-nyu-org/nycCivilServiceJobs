from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.


class ContactUsModel(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    subject = models.CharField(max_length=1000)
    message = models.TextField(validators=[MaxLengthValidator(5000)])

    class Meta:
        verbose_name_plural = "Contact Us"
