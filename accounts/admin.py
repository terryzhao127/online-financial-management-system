from django.contrib import admin

# Register your models here.
from .models import Staff


class StaffAdmin(admin.ModelAdmin):
    model = Staff
    filter_horizontal = ('workplaces',)


admin.site.register(Staff, StaffAdmin)
