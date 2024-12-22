from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def say_hello(Request):
    x = 1
    x = 2
    return render(Request, 'hello.html', {'name': 'mehrdad'})
