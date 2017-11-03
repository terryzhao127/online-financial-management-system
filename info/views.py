from django.shortcuts import render

# Create your views here.


def get_page(request):
    result = {
        'username': request.user.get_username(),
    }
    return render(request, 'info/info.html', result)
