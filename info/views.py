from django.http import HttpResponseRedirect
from django.shortcuts import render


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

    return render(request, 'info/info.html', result)

