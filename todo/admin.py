from django.contrib import admin

from .models import TODO

# Register your models here.
# admin.site.register(TODO)


@admin.register(TODO)
class TodoModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title",
                    "status", "date",  "priority"]
