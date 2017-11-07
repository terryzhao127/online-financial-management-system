from django.shortcuts import render


def error_404(request):
    # Test whether the user has logged in.
    if request.user.is_authenticated():
        return render(request, 'error_404_authenticated.html', status=404)
    else:
        return render(request, 'error_404.html', status=404)


def error_403(request, reason=""):
    # Test whether the user has logged in.
    if request.user.is_authenticated():
        return render(request, 'error_csrf_authenticated.html', status=403)
    else:
        return render(request, 'error_csrf.html', status=403)
