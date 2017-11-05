# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash


def custom_login(request):
    # Collect alerts.
    result = {}
    if 'alerts' in request.session:
        result['alerts'] = request.session['alerts']
        del request.session['alerts']

    # Test whether the user has logged in.
    if request.user.is_authenticated():
        return HttpResponseRedirect('/info/')
    else:
        return login(request, template_name='accounts/login.html', extra_context=result)


def change_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            result = {
                'alerts': [('success', 'Password changed!', 'Your password was successfully updated.')]
            }
            return render(request, 'info/info.html', result)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form,
    })
