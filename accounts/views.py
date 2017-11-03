from django.http import HttpResponseRedirect

# Create your views here.

from django.contrib.auth.views import login


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/info/')
    else:
        return login(request, 'accounts/login.html')
