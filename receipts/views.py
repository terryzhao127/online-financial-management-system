from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from companies.models import Company
from .models import Receipt, Item
from accounts.models import Staff
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import custom_error_404
from Online_Financial_Management_System.utils import redirect_with_data, __ITEMS_NUMBER_IN_A_PAGE, \
    get_slice_and_page_end
import math


@custom_login_required
def receipts(request, data, **kwargs):
    staff = Staff.objects.get(user=request.user)
    joined_workplaces = staff.workplaces.all()

    # Conditions on two kinds of url.
    if 'workplace_uuid' not in kwargs and 'page_num' not in kwargs:
        # No parameters

        # Test whether the staff has workplaces.
        if not joined_workplaces:
            data['no_workplaces'] = True
            return render(request, 'receipts/index.html', data)
        first_workplace_uuid = joined_workplaces[0].unique_id
        return redirect_with_data(request, data, '/receipts/' + str(first_workplace_uuid) + '/1/')
    else:
        # Two parameters
        data['no_workplaces'] = False
        data['joined_workplaces'] = joined_workplaces

        workplace_uuid = kwargs['workplace_uuid']
        page_num = kwargs['page_num']
        page_num = int(page_num)

        # If page number is zero.
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

        # Get all receipts in the company.
        receipt_records = Receipt.objects.filter(company=workplace)

        # If there is no receipt in company...
        if not receipt_records:
            data['no_receipt'] = True
        else:
            data['no_receipt'] = False

            # Get sliced records.
            data['receipt_records'], data['page_end'] = get_slice_and_page_end(receipt_records, page_num)

            # Get other necessary data
            data['page_range'] = range(1, data['page_end'] + 1)
            data['page_num'] = page_num

            # If sliced records are empty...
            if not data['receipt_records']:
                return custom_error_404(request, data)

        return render(request, 'receipts/index.html', data)


@custom_login_required
def details(request, data, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    data['receipt'] = receipt
    data['items'] = receipt.items.all()

    return render(request, 'receipts/details.html', data)


@custom_login_required
def create(request, data, **kwargs):
    if request.method == 'POST':
        # Get receipt data.
        creator = Staff.objects.get(user=request.user)
        payer = request.POST['payer']
        payee = request.POST['payee']
        date = request.POST['date']
        address = request.POST['address']
        notes = request.POST['notes']
        workplace = Company.objects.get(unique_id=request.POST['workplace_uuid'])

        # Create new Receipt instance.
        new_receipt = Receipt(creator=creator, payer=payer, payee=payee, total_amount=0, date=date,
                              address=address, notes=notes, company=workplace)
        new_receipt.save()

        # Get items data.
        for i in range(0, 7):
            if 'name_' + str(i) not in request.POST:
                break
            name = request.POST['name_' + str(i)]
            spec = request.POST['spec_' + str(i)]
            number = request.POST['number_' + str(i)]
            unit = request.POST['unit_' + str(i)]
            price = request.POST['price_' + str(i)]
            total_cost = request.POST['total_cost_' + str(i)]

            # Create new Item instance.
            new_item = Item(name=name, spec=spec, number=number, unit=unit, price=price, total_cost=total_cost)
            new_item.save()

            # Update receipt instance.
            new_receipt.items.add(new_item)
            new_receipt.total_amount += int(total_cost)
            new_receipt.save()

        # Success
        data['alerts'].append(('success', 'Create successfully!', 'You have successfully create a new receipt.'))
        return redirect_with_data(request, data, '/receipts/' + request.POST['workplace_uuid'] + '/1/')
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

        return render(request, 'receipts/create.html', data)


@custom_login_required
def delete(request, data):
    if request.method == 'POST':
        # Collect form data.
        receipt_id = request.POST['receipt_id']

        # Get Company instance.
        receipt = Receipt.objects.get(id=receipt_id)

        # Delete
        receipt.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a receipt.'))
        return redirect_with_data(request, data, '/receipts/' + request.POST['workplace_uuid'] + '/1/')
    else:
        return custom_error_404(request, data)
