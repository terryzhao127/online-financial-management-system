from django.shortcuts import render


def error_404(request):
    # Test whether the user has logged in.
    return render(request, 'error_404.html', status=404)


def error_403(request, reason=""):
    # Test whether the user has logged in.
    return render(request, 'error_csrf.html', status=403)
