from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from accounts.models import Staff
from companies.models import Company
from Online_Financial_Management_System.decorators import custom_login_required
from Online_Financial_Management_System.utils import redirect_with_data, render_alert_page_with_data
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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

        # Add new company to workplaces.
        owned_by.workplaces.add(new_company)

        # Success
        return render_alert_page_with_data(request, data, '/companies/'
                                  , ('success', 'Create successfully!', 'You have successfully create a new company.'))
    else:
        return render(request, 'companies/create_company.html', data)


@custom_login_required
def join_company(request, data):
    if request.method == 'POST':
        # Collect form data.
        unique_id = request.POST['unique_id']

        # Get Company instance.
        try:
            company = Company.objects.get(unique_id=unique_id)
        except ValidationError:
            data['alerts'].append(('error', 'Failed to join!', 'The UUID is invalid!'))
            return redirect_with_data(request, data, '/companies/join/')
        except ObjectDoesNotExist:
            data['alerts'].append(('error', 'Failed to join!', 'The company with this UUID does not exist!'))
            return redirect_with_data(request, data, '/companies/join/')

        # Add the company to workplaces.
        staff = Staff.objects.get(user=request.user)
        staff.workplaces.add(company)

        # Success
        return render_alert_page_with_data(request, data, '/companies/'
                                           , ('success', 'Join successfully!', 'You have successfully joined in a company.'))

    else:
        return render(request, 'companies/join_company.html', data)
