from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "dob",
        "email",
        "is_hiring_manager",
        "is_staff",
    )


admin.site.register(User, UserAdmin)
