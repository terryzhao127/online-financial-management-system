from django.shortcuts import render


def error_404(request):
    return render(request, 'errors/404.html', status=404)


def error_403(request):
    return render(request, 'errors/csrf.html', status=403)


def custom_error_404(request, data):
    return render(request, 'errors/404.html', data, status=404)
