from django.shortcuts import render
from splitapp.models import Group
from splitapp.models import User, Group, Expense, Transaction, Notification, ExpenseParticipants,GroupMembers
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

BOT_TOKEN = "7904198802:AAFam5t6n60kBnxBaANXOIHPshEZpmQX2wI"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_URL = " https://b794-5-114-110-217.ngrok-free.app"

def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/webhook"
    response = requests.get(f"{BASE_URL}/setWebhook", params={"url": webhook_url})
    if response.status_code == 200:
        print("Webhook set successfully.")
    else:
        print(f"Failed to set webhook: {response.status_code}, {response.text}")

@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        update = json.loads(request.body)
        print(update)
        if 'message' in update and 'web_app_data' in update['message']:
            user_id = update['message']['from']['id']
            data = update['message']['web_app_data']['data']  # This is the data sent from the Web App

            # Parse the data
            try:
                expenses = json.loads(data)  # Parse the JSON string into a Python list or dictionary
                print(f"User {user_id} sent expenses: {expenses}")
            except json.JSONDecodeError:
                print("Invalid JSON data received")

        data = json.loads(request.body)

        # Check if the message contains text
        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            first_name = data["message"]["chat"].get("first_name", "")
            text = data["message"]["text"]

            # Handle commands
            if text.startswith("/addexpense"):
                # Send a reply with a link to the mini app
                mini_app_url = f"{WEBHOOK_URL}/miniapp"
                reply_text = f"Please use this link to add an expense: {mini_app_url}"
            else:
                # Default response
                reply_text = f"hi {first_name}"

            send_message(chat_id, reply_text)

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "bad request"}, status=400)

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}, {response.text}")

def webapp(request):
    return render(request, 'add_expense.html')

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
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')

        user = User.objects.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password  # Password will be hashed by the manager
        )
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    return render(request, 'signup.html')


# Login View
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
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

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        group_id = str(uuid.uuid4())
        group = Group.objects.create(
            group_id=group_id,
            name=name
        )
        group.members.add(request.user)
        messages.success(request, 'Group created successfully.')
        return redirect('dashboard')
    return render(request, 'create_group.html')

@login_required
def add_user_to_group(request, group_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group = get_object_or_404(Group, group_id=group_id)
        user = get_object_or_404(User, user_id=user_id)
        GroupMembers.objects.create(group=group, user=user)
        messages.success(request, f'{user.name} added to group {group.name}.')
        return redirect('group_detail', group_id=group_id)

@login_required
def search_users(request):
    query = request.GET.get('query')
    group_id = request.GET.get('group_id')
    users = User.objects.filter(name__icontains=query)
    return render(request, 'search_users.html', {'users': users, 'group_id': group_id})

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
