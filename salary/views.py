from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def salary(request, data):
    return render(request, 'salary/salary.html', data)


@custom_login_required
def salary_details(request, data):
    return render(request, 'salary/salary_details.html', data)


@custom_login_required
def salary_manage(request, data):
    return render(request, 'salary/salary_manage.html', data)