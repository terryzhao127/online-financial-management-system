from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from .models import Receipt, Item
from accounts.models import Staff


@custom_login_required
def receipts(request, data):
    creator = Staff.objects.get(user=request.user)
    created_receipts = Receipt.objects.filter(creator=creator)

    if created_receipts:
        data['created_receipts'] = created_receipts
        data['no_receipt'] = False
    else:
        data['no_receipt'] = True

    return render(request, 'receipts/index.html', data)


@custom_login_required
def details(request, data):
    return render(request, 'receipts/details.html', data)


@custom_login_required
def create(request, data):
    return render(request, 'receipts/create.html')