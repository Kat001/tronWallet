from django.shortcuts import render

# Create your views here.


def index(request):
    d = {

    }
    return render(request, 'index.html', d)
