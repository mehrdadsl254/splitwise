from django.shortcuts import render
from splitapp.models import Group
from splitapp.models import User, Group, Expense, Transaction, Notification, ExpenseParticipants,GroupMembers
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def say_hello(Request):
    


    # def sign_in_user(user_id, name, email, phone=None):
    #     try:
    #         user, created = User.objects.get_or_create(
    #             user_id=user_id,
    #             defaults={'name': name, 'email': email, 'phone': phone}
    #         )
    #         if created:
    #             print("ysessssssssssssssssssssssssss")
    #             return {"status": "success", "message": "User signed in successfully", "user": user}
    #         else:
    #             return {"status": "info", "message": "User already exists", "user": user}
    #     except IntegrityError as e:
    #         return {"status": "error", "message": str(e)}
        
    
    # sign_in_user(15,"mehrdad","mehrdadsalehi254@gmail.com")
    return render(Request,'hello1.html')




# Home View
def home(request):
    return render(request, 'home.html')

# Sign-Up View
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')
        
        
        #increment by 1
        new_user_id = email
        user = User.objects.create(
            user_id=new_user_id,
            name=name,
            email=email,
            phone=phone,
        )
        user.save()
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    return render(request, 'signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            
            user = User.objects.get(email=email)
            # Here, you'd compare passwords or use a custom authentication
            
            login(request, user)  # Customize for session handling
            return redirect('dashboard')
            
        except User.DoesNotExist:
            return render(request, 'error.html', {'error': 'User not found.'})
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard View
@login_required
def dashboard(request):
    user = request.user
    groups = user.groups_involved.all()
    expenses = user.expenses_shared.all()
    notifications = Notification.objects.filter(receiver=user)

    context = {
        'user': user,
        'groups': groups,
        'expenses': expenses,
        'notifications': notifications,
    }
    return render(request, 'dashboard.html', context)

# Group List View
@login_required
def group_list(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'group_list.html', {'groups': groups})

# Group Detail View
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, group_id=group_id)
    members = group.members.all()
    expenses = group.expenses.all()

    context = {
        'group': group,
        'members': members,
        'expenses': expenses,
    }
    return render(request, 'group_detail.html', context)

# Add Expense View
@login_required
def add_expense(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')
        split_type = request.POST.get('split_type')
        payer_id = request.POST.get('payer')

        group = get_object_or_404(Group, group_id=group_id)
        payer = get_object_or_404(User, user_id=payer_id)

        expense = Expense.objects.create(
            expense_id=f"EXP_{timezone.now().timestamp()}",
            amount=amount,
            description=description,
            split_type=split_type,
            payer=payer,
            group=group,
        )
        expense.save()

        # Add participants (example logic for equal split)
        participants = group.members.all()
        for participant in participants:
            share = amount / len(participants)
            ExpenseParticipants.objects.create(expense=expense, user=participant, share=share)

        messages.success(request, 'Expense added successfully.')
        return redirect('group_detail', group_id=group_id)

    groups = request.user.groups_involved.all()
    return render(request, 'add_expense.html', {'groups': groups})

# Expense List View
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(participants=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})
