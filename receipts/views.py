from django.shortcuts import render
from django.http import HttpResponseRedirect


def get_page(request):
    # Test whether the user has logged in.
    if not request.user.is_authenticated():
        request.session['alerts'] = [('info', 'Ooops!', 'You have not logged in...')]
        return HttpResponseRedirect('/accounts/login/')

    # Collect alerts.
    result = {}
    if 'alerts' in request.session:
        result['alerts'] = request.session['alerts']
        del request.session['alerts']

    return render(request, 'receipt/receipt.html')
