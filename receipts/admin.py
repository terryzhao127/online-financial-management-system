from django.contrib import admin

# Register your models here.
from .models import Receipt, Item


class ReceiptAdmin(admin.ModelAdmin):
    model = Receipt
    filter_horizontal = ('items',)


admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Item)
