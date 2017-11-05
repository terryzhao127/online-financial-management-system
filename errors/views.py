from django.shortcuts import render


def error_404(request):
    # Test whether the user has logged in.
    if request.user.is_authenticated():
        return render(request, 'error_404_authenticated.html')
    else:
        return render(request, 'error_404.html')
