from django.contrib import admin
from .models import ContactUsModel


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        "contact_id",
        "name",
        "email",
        "subject",
        "message",
    )
    list_filter = ["email"]
    search_fields = ["subject"]


# Register your models here.
admin.site.register(ContactUsModel, ContactUsAdmin)
