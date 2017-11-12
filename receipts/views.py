from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def receipts(request, data):
    return render(request, 'receipts/index.html', data)


@custom_login_required
def details(request, data):
    return render(request, 'receipts/details.html', data)


@custom_login_required
def create(request, data):
    return render(request, 'receipts/create.html')