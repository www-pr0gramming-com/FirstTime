from django.contrib import admin
from .models import User, A001, Agent, UserProfile, Category


class A001Admin(admin.ModelAdmin):
    fields = (
        "first_name",
        "last_name",
    )

    list_display = ["id", "first_name", "last_name", "age", "email"]
    list_editable = ["first_name"]
    list_filter = ["category"]
    search_fields = ["first_name"]


admin.site.register(User)
admin.site.register(A001, A001Admin)
admin.site.register(Agent)
admin.site.register(UserProfile)
admin.site.register(Category)
