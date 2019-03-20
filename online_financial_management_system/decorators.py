from django.http import HttpResponseRedirect
from online_financial_management_system import utils


def custom_login_required(view_func):
    def wrapper(request, *args, **kw):
        # Collect alerts.
        alerts = utils.get_alerts(request)

        # Require login
        if not request.user.is_authenticated():
            alerts.append(('info', 'Ooops!', 'You have not logged in...'))
            request.session['alerts'] = alerts
            return HttpResponseRedirect('/accounts/login')

        data = {'alerts': alerts}
        return view_func(request, data, *args, **kw)

    return wrapper
