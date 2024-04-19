from django.shortcuts import render
from django.http import HttpResponse
from lipReadingDataset.models import TextData

# Create your views here.

def say_hello(request):
    return render(request, 'home.html', {'name':'Usman'})
