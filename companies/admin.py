from django.contrib import admin
from .models import Company

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    filter_horizontal = ('staff',)
    list_display = ['name', 'owner', 'unique_id']


admin.site.register(Company, CompanyAdmin)
