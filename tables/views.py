from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def tables(request, data):
    return render(request, 'tables/tables.html', data)


@custom_login_required
def details(request, data):
    return render(request, 'tables/table_details.html', data)
