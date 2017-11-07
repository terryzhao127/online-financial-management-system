from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Information
from salary.models import Salary


def get_page(request):
    # Test whether the user has logged in.
    if not request.user.is_authenticated():
        request.session['alerts'] = [('info', 'Ooops!', 'You have not logged in...')]
        return HttpResponseRedirect('/accounts/login/')

    data = {}

    # Collect alerts.
    if 'alerts' in request.session:
        data['alerts'] = request.session['alerts']
        del request.session['alerts']

    # Collect information of user.
    info_of_user = Information.objects.get(user=request.user)
    data['full_name'] = info_of_user.name
    data['age'] = info_of_user.age
    data['photo'] = info_of_user.photo

    # Collect salary of user
    salary_of_user = Salary.objects.get(user=request.user)
    data['bonus'] = salary_of_user.bonus
    data['bonus_date'] = salary_of_user.bonus_date
    data['salary_amount'] = salary_of_user.amount
    data['paid_method'] = salary_of_user.paid_method

    return render(request, 'info/info.html', data)
