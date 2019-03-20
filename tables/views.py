from django.shortcuts import render
from online_financial_management_system.decorators import custom_login_required
from online_financial_management_system.utils import redirect_with_data, get_slice_and_page_end
from accounts.models import Staff
from errors.views import custom_error_404
from companies.models import Company
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Table, Item


@custom_login_required
def tables(request, data, **kwargs):
    staff = Staff.objects.get(user=request.user)
    joined_workplaces = staff.workplaces.all()

    # Conditions on two kinds of url.
    if 'workplace_uuid' not in kwargs and 'page_num' not in kwargs:
        # No parameters

        # Test whether the staff has workplaces.
        if not joined_workplaces:
            data['no_workplaces'] = True
            return render(request, 'tables/index.html', data)

        first_workplace_uuid = joined_workplaces[0].unique_id
        return redirect_with_data(request, data, '/tables/' + str(first_workplace_uuid) + '/1/')
    else:
        # Two parameters

        data['no_workplaces'] = False
        data['joined_workplaces'] = joined_workplaces
        
        workplace_uuid = kwargs['workplace_uuid']
        page_num = kwargs['page_num']
        page_num = int(page_num)

        # If page number is zero...
        if page_num == 0:
            return custom_error_404(request, data)

        # If workplace_uuid is invalid...
        try:
            workplace = Company.objects.get(unique_id=workplace_uuid)
        except ValidationError:
            return custom_error_404(request, data)
        except ObjectDoesNotExist:
            return custom_error_404(request, data)

        # Get UUID.
        data['workplace_uuid'] = workplace.unique_id

        # Get all tables in the company.
        table_records = Table.objects.filter(company=workplace)

        # If there is no table record in company...
        if not table_records:
            data['no_table_records'] = True
        else:
            data['no_table_records'] = False

            # Get sliced records.
            data['table_records'], data['page_end'] = get_slice_and_page_end(table_records, page_num)

            # Get other necessary data.
            data['page_range'] = range(1, data['page_end'] + 1)
            data['page_num'] = page_num

            # If sliced records are empty...
            if not data['table_records']:
                return custom_error_404(request, data)

    return render(request, 'tables/index.html', data)


@custom_login_required
def details(request, data, table_id):
    # If table_id is invalid...
    try:
        table_record = Table.objects.get(id=table_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    data['table'] = table_record
    data['items'] = table_record.items.all()
    return render(request, 'tables/details.html', data)


@custom_login_required
def create(request, data, **kwargs):
    if request.method == 'POST':
        # Get table data.
        creator = Staff.objects.get(user=request.user)
        workplace = Company.objects.get(unique_id=request.POST['workplace_uuid'])
        table_name = request.POST['table_name']
        date = request.POST['date']

        # Create new Table instance.
        new_table = Table(creator=creator, company=workplace, date=date, name=table_name)
        new_table.save()

        # Get items data.
        i = 0
        while 'item_name_' + str(i) in request.POST:
            item_name = request.POST['item_name_' + str(i)]
            money_change = request.POST['item_money_change_' + str(i)]

            # Create new Item instance
            new_item = Item(name=item_name, money_change=money_change)
            new_item.save()

            # Update receipt instance.
            new_table.items.add(new_item)

            i = i + 1

        # Success
        data['alerts'].append(('success', 'Create successfully!', 'You have successfully create a new table.'))
        return redirect_with_data(request, data, '/tables/' + request.POST['workplace_uuid'] + '/1/')
    else:
        if 'workplace_uuid' not in kwargs:
            return custom_error_404(request, data)

        workplace_uuid = kwargs['workplace_uuid']

        # If workplace_uuid is invalid...
        try:
            workplace = Company.objects.get(unique_id=workplace_uuid)
        except ValidationError:
            return custom_error_404(request, data)
        except ObjectDoesNotExist:
            return custom_error_404(request, data)

        # Get UUID.
        data['workplace_uuid'] = workplace.unique_id

    return render(request, 'tables/create.html', data)


@custom_login_required
def delete(request, data):
    if request.method == 'POST':
        # Collect form data.
        table_id = request.POST['table_id']

        # Get Salary instance.
        table_record = Table.objects.get(id=table_id)

        # Delete
        table_record.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a table.'))
        return redirect_with_data(request, data, '/tables/' + request.POST['workplace_uuid'] + '/1/')
    else:
        return custom_error_404(request, data)


@custom_login_required
def update(request, data, table_id):
    # Get table instance.
    try:
        table_record = Table.objects.get(id=table_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    if request.method == 'POST':
        # Update table data.
        table_record.name = request.POST['table_name']
        table_record.date = request.POST['date']
        table_record.save()

        # Update items data.
        for i, item in enumerate(table_record.items.all()):
            item.name = request.POST['item_name_' + str(i)]
            item.money_change = request.POST['item_money_change_' + str(i)]
            item.save()

        # Success
        data['alerts'].append(('success', 'Update successfully!', 'You have successfully update a table.'))
        return redirect_with_data(request, data, '/tables/details/' + table_id + '/')
    else:
        data['table'] = table_record
        return render(request, 'tables/update.html', data)