from django.shortcuts import render

# Create your views here.
from accounts.models import Staff
from companies.models import Company
from Online_Financial_Management_System.decorators import custom_login_required
from Online_Financial_Management_System.utils import redirect_with_data, ITEMS_NUMBER_IN_A_PAGE
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import error_404 as custom_error_404
import math


@custom_login_required
def companies(request, data, workplaces_page_num, owned_companies_page_num):
    workplaces_page_num = int(workplaces_page_num)
    owned_companies_page_num = int(owned_companies_page_num)

    # If page number is zero.
    if workplaces_page_num == 0 or owned_companies_page_num == 0:
        return custom_error_404(request, data)

    # Collect information of companies.
    staff = Staff.objects.get(user=request.user)
    workplaces = staff.workplaces.all()
    if not workplaces:
        data['no_workplace'] = True
    else:
        # Calculate the list area indices.
        workplaces_start = (workplaces_page_num - 1) * ITEMS_NUMBER_IN_A_PAGE
        workplaces_end = workplaces_page_num * ITEMS_NUMBER_IN_A_PAGE

        data['no_workplace'] = False
        data['workplaces_page_end'] = math.ceil(len(workplaces) / ITEMS_NUMBER_IN_A_PAGE)
        data['workplaces_page_range'] = range(1, data['workplaces_page_end'] + 1)
        data['workplaces'] = workplaces[workplaces_start:workplaces_end]
    data['workplaces_page_num'] = workplaces_page_num

    owned_companies = Company.objects.filter(owner=staff)
    if not owned_companies:
        data['no_owned_company'] = True
    else:
        # Calculate the list area indices.
        owned_companies_start = (owned_companies_page_num - 1) * ITEMS_NUMBER_IN_A_PAGE
        owned_companies_end = owned_companies_page_num * ITEMS_NUMBER_IN_A_PAGE

        data['no_owned_company'] = False
        data['owned_companies_page_end'] = math.ceil(len(owned_companies) / ITEMS_NUMBER_IN_A_PAGE)
        data['owned_companies_page_range'] = range(1, data['owned_companies_page_end'] + 1)
        data['owned_companies'] = owned_companies[owned_companies_start:owned_companies_end]
    data['owned_companies_page_num'] = owned_companies_page_num

    # If either table is empty while companies set are not empty... (Due to invalid page num)
    if 'workplaces' in data and not data['workplaces'] or 'owned_companies' in data and not data['owned_companies']:
        return custom_error_404(request, data)

    return render(request, 'companies/index.html', data)


@custom_login_required
def create(request, data):
    if request.method == 'POST':
        # Collect form data.
        company_name = request.POST['company_name']
        owned_by = Staff.objects.get(user=request.user)

        # Create new Company instance.
        new_company = Company(name=company_name, owner=owned_by)
        new_company.save()

        # Add new company to workplaces.
        owned_by.workplaces.add(new_company)

        # Add owner to staff of new company.
        new_company.staff.add(owned_by)

        # Success
        data['alerts'].append(('success', 'Create successfully!', 'You have successfully create a new company.'))
        return redirect_with_data(request, data, '/companies/')
    else:
        return render(request, 'companies/create.html', data)


@custom_login_required
def join(request, data):
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

        # Add staff instance to staff field of company.
        company.staff.add(staff)

        # Test whether the user has already joined the company.
        if company in staff.workplaces.all():
            data['alerts'].append(('warning', 'Failed to join.', 'You have already joined in this company!'))
            return redirect_with_data(request, data, '/companies/')

        staff.workplaces.add(company)

        # Success
        data['alerts'].append(('success', 'Join successfully!', 'You have successfully joined in a company.'))
        return redirect_with_data(request, data, '/companies/')
    else:
        return render(request, 'companies/join.html', data)


@custom_login_required
def delete(request, data):
    if request.method == 'POST':
        # Collect form data.
        unique_id = request.POST['unique_id']

        # Get Company instance.
        company = Company.objects.get(unique_id=unique_id)

        # Delete
        company.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a company.'))
        return redirect_with_data(request, data, '/companies/')
    else:
        return custom_error_404(request, data)


@custom_login_required
def details(request, data, company_uuid):
    # Get Company instance.
    data['company'] = Company.objects.get(unique_id=company_uuid)

    # Get permission.
    staff = Staff.objects.get(user=request.user)
    if staff == data['company'].owner:
        data['is_owner'] = True
    else:
        data['is_owner'] = False

    return render(request, 'companies/details.html', data)
