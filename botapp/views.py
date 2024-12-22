from django.shortcuts import render
from splitapp.models import Group
from splitapp.models import User, Group, Expense, Transaction, Notification, ExpenseParticipants
from django.utils import timezone
from django.db import IntegrityError
# Create your views here.
def say_hello(Request):
    


    def sign_in_user(user_id, name, email, phone=None):
        try:
            user, created = User.objects.get_or_create(
                user_id=user_id,
                defaults={'name': name, 'email': email, 'phone': phone}
            )
            if created:
                print("ysessssssssssssssssssssssssss")
                return {"status": "success", "message": "User signed in successfully", "user": user}
            else:
                return {"status": "info", "message": "User already exists", "user": user}
        except IntegrityError as e:
            return {"status": "error", "message": str(e)}
        
    
    sign_in_user(15,"mehrdad","mehrdadsalehi254@gmail.com")
    return render(Request, 'hello.html')

# def say_hello(Request):
#     group = Group.objects.get(pk = 'G001')
#     name = group.name
#     return render(Request, 'hello.html')