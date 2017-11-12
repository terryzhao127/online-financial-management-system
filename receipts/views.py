from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from .models import Receipt, Item
from accounts.models import Staff
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import error_404 as custom_error_404
from Online_Financial_Management_System.utils import ITEMS_NUMBER_IN_A_PAGE
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
        start = (page_num - 1) * ITEMS_NUMBER_IN_A_PAGE
        end = page_num * ITEMS_NUMBER_IN_A_PAGE

        data['no_receipt'] = False
        data['page_end'] = math.ceil(len(created_receipts) / ITEMS_NUMBER_IN_A_PAGE)
        data['page_range'] = range(1, data['page_end'] + 1)
        data['created_receipts'] = created_receipts[start:end]
        data['page_num'] = page_num

    return render(request, 'receipts/index.html', data)


@custom_login_required
def details(request, data, receipt_id):
    try:
        receipt = Receipt.objects.get(id=receipt_id)
    except ValidationError:
        return error_404(request, data)
    except ObjectDoesNotExist:
        return error_404(request, data)

    data['receipt'] = receipt
    data['items'] = receipt.items.all()

    return render(request, 'receipts/details.html', data)


@custom_login_required
def create(request, data):
    return render(request, 'receipts/create.html')