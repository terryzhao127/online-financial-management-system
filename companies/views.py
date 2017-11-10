from django.shortcuts import render

# Create your views here.
from accounts.models import Staff
from companies.models import Company
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    # Collect information of companies.
    staff = Staff.objects.get(user=request.user)
    data['workplaces'] = staff.workplaces.all()

    owned_companies = Company.objects.filter(owner=staff)
    data['owned_companies'] = owned_companies

    return render(request, 'companies/companies.html', data)


@custom_login_required
def create_company(request, data):
    if request.method == 'POST':
        # Collect form data.
        company_name = request.POST['company_name']
        owned_by = Staff.objects.get(user=request.user)

        # Create new Company instance.
        new_company = Company(name=company_name, owner=owned_by)
        new_company.save()

        data['alert'] = ('success', 'Create successfully!', 'You have successfully create a new company.')
        data['redirect_link'] = '/companies/'
        return render(request, 'alert_and_redirect.html', data)
    else:
        return render(request, 'companies/create_company.html', data)


def join_company(request):
    pass
