from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def receipts(request, data):
    return render(request, 'receipts/receipts.html', data)


@custom_login_required
def receipt_details(request, data):
    return render(request, 'receipts/receipts_details.html', data)
