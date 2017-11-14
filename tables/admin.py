from django.contrib import admin

# Register your models here.
from .models import Table, Item


class TableAdmin(admin.ModelAdmin):
    model = Table
    filter_horizontal = ('items',)


admin.site.register(Table, TableAdmin)
admin.site.register(Item)
