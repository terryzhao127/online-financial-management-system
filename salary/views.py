import math
from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from Online_Financial_Management_System.utils import ITEMS_NUMBER_IN_A_PAGE, redirect_with_data
from accounts.models import Staff
from companies.models import Company
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import error_404 as custom_error_404
from salary.models import Salary


@custom_login_required
def salary(request, data, **kwargs):
    data['no_owned_company'] = False
    payer = Staff.objects.get(user=request.user)
    owned_companies = Company.objects.filter(owner=payer)

    if 'company_uuid' not in kwargs and 'page_num' not in kwargs:
        # Test whether the staff has companies.
        if not owned_companies:
            data['no_owned_company'] = True
            return render(request, 'salary/index.html', data)

        first_company_uuid_str = owned_companies.all()[0].unique_id
        return redirect_with_data(request, data, '/salary/' + str(first_company_uuid_str) + '/1/')
    else:
        company_uuid = kwargs['company_uuid']
        page_num = kwargs['page_num']
        page_num = int(page_num)

        # If page number is zero...
        if page_num == 0:
            return custom_error_404(request, data)

        # If company_uuid is invalid...
        try:
            company = Company.objects.get(unique_id=company_uuid)
        except ValidationError:
            return custom_error_404(request, data)
        except ObjectDoesNotExist:
            return custom_error_404(request, data)

        # If the logged staff is not the owner of the company:
        if company.owner != payer:
            return custom_error_404(request, data)

        # Get all salary belonging to staffs in the same company.
        salary_records = Salary.objects.filter(company=company)

        if not salary_records:
            data['no_salary_records'] = True
        else:
            data['no_salary_records'] = False

            # Calculate the list area indices.
            start = (page_num - 1) * ITEMS_NUMBER_IN_A_PAGE
            end = page_num * ITEMS_NUMBER_IN_A_PAGE

            data['page_end'] = math.ceil(len(salary_records) / ITEMS_NUMBER_IN_A_PAGE)
            data['page_range'] = range(1, data['page_end'] + 1)
            data['page_num'] = page_num
            data['salary_records'] = salary_records[start:end]

            if not data['salary_records']:
                return custom_error_404(request, data)

        data['owned_companies'] = owned_companies
        data['company_uuid'] = company.unique_id

    return render(request, 'salary/index.html', data)


@custom_login_required
def details(request, data, salary_id):
    try:
        salary_record = Salary.objects.get(id=salary_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    data['salary'] = salary_record
    return render(request, 'salary/details.html', data)


@custom_login_required
def delete(request, data):
    if request.method == 'POST':
        # Collect form data.
        salary_id = request.POST['salary_id']

        # Get Salary instance.
        salary_record = Salary.objects.get(id=salary_id)

        # Delete
        salary_record.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a record of salary.'))
        return redirect_with_data(request, data, '/salary/')
    else:
        return custom_error_404(request, data)


@custom_login_required
def create(request, data):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'salary/create.html', data)