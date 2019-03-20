from django.shortcuts import render
from online_financial_management_system.decorators import custom_login_required
from companies.models import Company
from .models import Receipt, Item
from accounts.models import Staff
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import custom_error_404
from online_financial_management_system.utils import redirect_with_data, __ITEMS_NUMBER_IN_A_PAGE, \
    get_slice_and_page_end


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

        # Get Receipt instance.
        receipt = Receipt.objects.get(id=receipt_id)

        # Delete
        receipt.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a receipt.'))
        return redirect_with_data(request, data, '/receipts/' + request.POST['workplace_uuid'] + '/1/')
    else:
        return custom_error_404(request, data)


@custom_login_required
def update(request, data, receipt_id):
    # Get receipt instance.
    try:
        receipt = Receipt.objects.get(id=receipt_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)
    items = receipt.items.all()

    if request.method == 'POST':
        # Get form data.
        creator = Staff.objects.get(user=request.user)
        payer = request.POST['payer']
        payee = request.POST['payee']
        date = request.POST['date']
        address = request.POST['address']
        notes = request.POST['notes']

        # Update receipt.
        receipt.creator = creator
        receipt.payee = payee
        receipt.payer = payer
        receipt.date = date
        receipt.address = address
        receipt.notes = notes
        receipt.save()

        # Update items.
        for i, item in enumerate(items):
            if 'name_' + str(i) not in request.POST:
                break
            name = request.POST['name_' + str(i)]
            spec = request.POST['spec_' + str(i)]
            number = request.POST['number_' + str(i)]
            unit = request.POST['unit_' + str(i)]
            price = request.POST['price_' + str(i)]
            total_cost = request.POST['total_cost_' + str(i)]

            # Update item instance.
            item.name = name
            item.spec = spec
            item.number = number
            item.unit = unit
            item.price = price
            item.total_cost = total_cost
            item.save()

        # Update total amount of receipt.
        total_amount = 0
        for item in receipt.items.all():
            total_amount += item.total_cost
        receipt.total_amount = total_amount
        receipt.save()

        # Success
        data['alerts'].append(('success', 'Update successfully!', 'You have successfully updated a receipt.'))
        return redirect_with_data(request, data, '/receipts/details/' + receipt_id + '/')
    else:
        data['receipt'] = receipt

        # Generate names and ids for input tag.
        frontend_fields = {
            'name': 'update-receipt-item-name-',
            'spec': 'update-receipt-item-spec-',
            'number': 'update-receipt-item-number-',
            'unit': 'update-receipt-item-unit-',
            'price': 'update-receipt-item-price-',
            'total_cost': 'update-receipt-item-total-cost-',
        }

        backend_fields = {
            'name': 'name_',
            'spec': 'spec_',
            'number': 'number_',
            'unit': 'unit_',
            'price': 'price_',
            'total_cost': 'total_cost_',
        }

        item_containers = []
        for i, item in enumerate(items):
            container = {'item': item}
            front_temp = {}
            for key, value in frontend_fields.items():
                front_temp[key] = frontend_fields[key] + str(i)
            container['frontend_fields'] = front_temp

            back_temp = {}
            for key, value in backend_fields.items():
                back_temp[key] = backend_fields[key] + str(i)
            container['backend_fields'] = back_temp

            item_values = {'name': item.name,
                           'spec': item.spec,
                           'number': item.number,
                           'unit': item.unit,
                           'price': item.price,
                           'total_cost': item.total_cost}
            container['item_values'] = item_values

            item_containers.append(container)

        data['item_containers'] = item_containers

        return render(request, 'receipts/update.html', data)
