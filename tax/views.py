from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required


@custom_login_required
def get_page(request, data):
    return render(request, 'tax/tax.html', data)
