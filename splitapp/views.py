from django.shortcuts import render
from splitapp.models import Group
# Create your views here.
def say_hello(Request):
    group = Group.objects.get(pk = 'G001')
    name = group.name
    return render(Request, 'hello.html', {'name': group})
