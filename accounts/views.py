from django.http import HttpResponseRedirect
from django.contrib.auth import login as direct_login
from django.contrib.auth import authenticate
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from online_financial_management_system.utils import get_alerts, render_alert_page_with_data, redirect_with_data
from accounts.forms import SignUpForm
from online_financial_management_system.decorators import custom_login_required


def custom_login(request):
    data = {}

    # Collect alerts.
    alerts = get_alerts(request)
    data['alerts'] = alerts

    # Test whether the user has logged in.
    if request.user.is_authenticated():
        return redirect_with_data(request, data, '/info/')
    else:
        return login(request, template_name='accounts/login.html', extra_context=data)


@custom_login_required
def custom_logout(request, data):
    data['alert'] = ('success', 'Logout successfully!', 'You have successfully logged out!')
    data['redirect_link'] = '/index/'
    return logout(request, template_name='alert_and_redirect.html', extra_context=data)


@custom_login_required
def change_password(request, data):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            # Success
            data['alerts'].append(('success', 'Password changed!', 'Your password was successfully updated.'))
            return render(request, 'info/index.html', data)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form}, data)


def signup(request):
    # Collect alerts.
    alerts = get_alerts(request)

    # Test whether the user has logged in.
    if request.user.is_authenticated():
        alerts.append(('info', 'You have logged in!', 'If you want to sign up a new account, please log out first.'))
        request.session['alerts'] = alerts
        return HttpResponseRedirect('/info/')

    data = {'alerts': alerts}

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the staff instance created by the signal
            user.staff.full_name = form.cleaned_data.get('full_name')
            user.staff.age = form.cleaned_data.get('age')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            direct_login(request, user)
            return redirect_with_data(request, data, '/info/')
    else:
        form = SignUpForm()

    data['form'] = form
    return render(request, 'accounts/signup.html', data)
