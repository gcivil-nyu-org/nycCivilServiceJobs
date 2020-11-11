from django.contrib import admin

from .models import UsersCivilServiceTitle


class UsersCivilServiceTitleAdmin(admin.ModelAdmin):
    list_display = ("civil_service_title", "user", "is_interested")


admin.site.register(UsersCivilServiceTitle, UsersCivilServiceTitleAdmin)
