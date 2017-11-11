from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    return render(request, 'salary/salary.html', data)


@custom_login_required
def upload_file(request, data):
    return render(request, 'salary/upload.html', data)


@custom_login_required
def details(request, data):
    return render(request, 'salary/salary_details.html', data)