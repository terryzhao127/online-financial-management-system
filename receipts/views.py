from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from .models import Receipt, Item
from accounts.models import Staff
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import custom_error_404
from Online_Financial_Management_System.utils import redirect_with_data, __ITEMS_NUMBER_IN_A_PAGE
import math


@custom_login_required
def receipts(request, data, page_num):
    page_num = int(page_num)

    # If page number is zero.
    if page_num == 0:
        return custom_error_404(request, data)

    # Collect information of receipts.
    staff = Staff.objects.get(user=request.user)
    created_receipts = Receipt.objects.filter(creator=staff)

    if not created_receipts:
        data['no_receipt'] = True
    else:
        # Calculate the list area indices.
        start = (page_num - 1) * __ITEMS_NUMBER_IN_A_PAGE
        end = page_num * __ITEMS_NUMBER_IN_A_PAGE

        data['no_receipt'] = False
        data['page_end'] = math.ceil(len(created_receipts) / __ITEMS_NUMBER_IN_A_PAGE)
        data['page_range'] = range(1, data['page_end'] + 1)
        data['page_num'] = page_num
        data['created_receipts'] = created_receipts[start:end]

        if not data['created_receipts']:
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
def create(request, data):
    if request.method == 'POST':
        # Get receipt data.
        creator = Staff.objects.get(user=request.user)
        payer = request.POST['payer']
        payee = request.POST['payee']
        date = request.POST['date']
        address = request.POST['address']
        notes = request.POST['notes']

        # Create new Receipt instance.
        new_receipt = Receipt(creator=creator, payer=payer, payee=payee, total_amount=0, date=date,
                              address=address, notes=notes)
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
        return redirect_with_data(request, data, '/receipts/')
    else:
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
        return redirect_with_data(request, data, '/receipts/')
    else:
        return custom_error_404(request, data)
