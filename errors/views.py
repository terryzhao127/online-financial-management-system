from django.shortcuts import render


def error_404(request):
    return render(request, 'errors/404.html', status=404)


def error_403(request, reason=""):
    return render(request, 'errors/csrf.html', status=403)
