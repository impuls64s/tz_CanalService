from django.shortcuts import render
from .first_app.models import FirstApp


def index(request):
    queryset = FirstApp.objects.all().order_by('id')
    return render(request, 'index.html', context={
        'data': queryset
    })
