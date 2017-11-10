from django.shortcuts import render


def error_404(request):
    return render(request, 'error_404.html', status=404)


def error_403(request, reason=""):
    return render(request, 'error_csrf.html', status=403)
