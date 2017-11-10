from django.shortcuts import render
from accounts.models import Staff
from companies.models import Company
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    # Collect information of staff.
    staff = Staff.objects.get(user=request.user)
    data['full_name'] = staff.full_name
    data['age'] = staff.age
    data['workplaces'] = staff.workplaces.all()

    owned_companies = Company.objects.filter(owner=staff)
    data['owned_companies'] = owned_companies

    return render(request, 'info/info.html', data)
