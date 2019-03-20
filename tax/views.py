from django.shortcuts import render
from online_financial_management_system.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    return render(request, 'tax/index.html', data)
