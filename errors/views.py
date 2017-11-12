from django.shortcuts import render


def error_404(request, data):
    return render(request, 'errors/404.html', data, status=404)


def error_403(request, data):
    return render(request, 'errors/csrf.html', data, status=403)
