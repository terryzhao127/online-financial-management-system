from django.shortcuts import render

# Create your views here.
from accounts.models import Staff
from companies.models import Company
from online_financial_management_system.decorators import custom_login_required
from online_financial_management_system.utils import redirect_with_data, __ITEMS_NUMBER_IN_A_PAGE
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import custom_error_404
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
        workplaces_start = (workplaces_page_num - 1) * __ITEMS_NUMBER_IN_A_PAGE
        workplaces_end = workplaces_page_num * __ITEMS_NUMBER_IN_A_PAGE

        data['no_workplace'] = False
        data['workplaces_page_end'] = math.ceil(len(workplaces) / __ITEMS_NUMBER_IN_A_PAGE)
        data['workplaces_page_range'] = range(1, data['workplaces_page_end'] + 1)
        data['workplaces'] = workplaces[workplaces_start:workplaces_end]
    data['workplaces_page_num'] = workplaces_page_num

    owned_companies = Company.objects.filter(owner=staff)
    if not owned_companies:
        data['no_owned_company'] = True
    else:
        # Calculate the list area indices.
        owned_companies_start = (owned_companies_page_num - 1) * __ITEMS_NUMBER_IN_A_PAGE
        owned_companies_end = owned_companies_page_num * __ITEMS_NUMBER_IN_A_PAGE

        data['no_owned_company'] = False
        data['owned_companies_page_end'] = math.ceil(len(owned_companies) / __ITEMS_NUMBER_IN_A_PAGE)
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
        return redirect_with_data(request, data, '/companies/1+1/#tab2')
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
            return redirect_with_data(request, data, '/companies/1+1/#tab1')

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
    try:
        data['company'] = Company.objects.get(unique_id=company_uuid)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    # Get permission.
    staff = Staff.objects.get(user=request.user)
    if staff == data['company'].owner:
        data['is_owner'] = True
    else:
        data['is_owner'] = False

    # Get number of staff.
    data['staff_number'] = len(data['company'].staff.all())

    return render(request, 'companies/details.html', data)


@custom_login_required
def leave(request, data):
    if request.method == 'POST':
        # Get form data.
        unique_id = request.POST['unique_id']

        # Get Company instance.
        company = Company.objects.get(unique_id=unique_id)

        # Get Staff instance.
        staff = Staff.objects.get(user=request.user)

        # Quit
        staff.workplaces = staff.workplaces.all().exclude(unique_id=unique_id)
        staff.save()
        company.staff = company.staff.all().exclude(user=request.user)
        company.save()

        # Success
        data['alerts'].append(('success', 'Quit successfully!', 'You have successfully quited a company.'))
        return redirect_with_data(request, data, '/companies/1+1/#tab1')
    else:
        return custom_error_404(request, data)


@custom_login_required
def update(request, data, company_uuid):
    # Get Company instance.
    try:
        company = Company.objects.get(unique_id=company_uuid)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    if request.method == 'POST':
        # Get form data.
        name = request.POST['name']

        # Update company.
        company.name = name
        company.save()

        # Success
        data['alerts'].append(
            ('success', 'Update successfully!', 'You have successfully updated information of a company.'))
        return redirect_with_data(request, data, '/companies/details/' + company_uuid + '/')
    else:
        data['company'] = company
        return render(request, 'companies/update.html', data)


@custom_login_required
def render_staff_page(request, data, company_uuid):
    # Get staff.
    try:
        company = Company.objects.get(unique_id=company_uuid)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    data['staff'] = company.staff.all().exclude(user=request.user)
    data['company'] = company

    return render(request, 'companies/manage.html', data)


@custom_login_required
def fire_staff(request, data):
    if request.method == 'POST':
        # Collect form data.
        unique_id = request.POST['unique_id']
        employer_id = request.POST['employer_id']

        # Get Company instance.
        company = Company.objects.get(unique_id=unique_id)

        # Get Staff instance.
        employee = Staff.objects.get(id=employer_id)

        # Fire
        company.staff = company.staff.all().exclude(id=employer_id)
        company.save()
        employee.workplaces = employee.workplaces.all().exclude(unique_id=unique_id)
        employee.save()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully fired an employee.'))
        return redirect_with_data(request, data, '/companies/manage/' + unique_id + '/')
    else:
        return custom_error_404(request, data)
