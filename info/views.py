from django.shortcuts import render
from accounts.models import Staff
from companies.models import Company
from salary.models import Salary
from django.core.exceptions import ObjectDoesNotExist
from online_financial_management_system.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    # Collect basic information of staff.
    staff = Staff.objects.get(user=request.user)
    data['full_name'] = staff.full_name
    data['age'] = staff.age

    # Collect companies information.
    data['workplaces'] = staff.workplaces.all()
    owned_companies = Company.objects.filter(owner=staff)
    data['owned_companies'] = owned_companies

    # Collect salary information.
    data['salary_records'] = Salary.objects.filter(payee=staff)

    return render(request, 'info/index.html', data)
