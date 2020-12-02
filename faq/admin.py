from django.contrib import admin
from .models import faq


# Register your models here.
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        "faq_id",
        "question",
        "answer",
        "date_published",
    )
    list_filter = ["date_published"]
    search_fields = ["question"]


admin.site.register(faq, FAQAdmin)
