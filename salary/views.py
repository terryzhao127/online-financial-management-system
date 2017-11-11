from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def salary(request, data):
    return render(request, 'salary/salary.html', data)


@custom_login_required
def upload(request, data):
    return render(request, 'salary/upload.html', data)


@custom_login_required
def details(request, data):
    return render(request, 'salary/details.html', data)