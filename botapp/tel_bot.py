from splitapp.models import User, Group, Expense, Transaction, Notification, ExpenseParticipants
from django.utils import timezone
from django.db import IntegrityError

# Sign in user
def sign_in_user(user_id, name, email, phone=None):
    try:
        user, created = User.objects.get_or_create(
            user_id=user_id,
            defaults={'name': name, 'email': email, 'phone': phone}
        )
        if created:
            return {"status": "success", "message": "User signed in successfully", "user": user}
        else:
            return {"status": "info", "message": "User already exists", "user": user}
    except IntegrityError as e:
        return {"status": "error", "message": str(e)}

# Add user to a group
def add_user_to_group(user_id, group_id, group_name):
    try:
        user = User.objects.get(user_id=user_id)
        group, created = Group.objects.get_or_create(group_id=group_id, defaults={'name': group_name})
        group.members.add(user)
        return {"status": "success", "message": f"User {user.name} added to group {group.name}"}
    except User.DoesNotExist:
        return {"status": "error", "message": "User does not exist"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Add expense
def add_expense(payer_id, group_id, amount, description, split_type="EQUAL", participant_ids=None):
    try:
        payer = User.objects.get(user_id=payer_id)
        group = Group.objects.get(group_id=group_id)
        expense = Expense.objects.create(
            expense_id=f"{group_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            amount=amount,
            description=description,
            split_type=split_type,
            payer=payer,
            group=group
        )
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            for participant in participants:
                ExpenseParticipants.objects.create(expense=expense, user=participant)
        return {"status": "success", "message": "Expense added successfully", "expense": expense}
    except User.DoesNotExist:
        return {"status": "error", "message": "Payer or participant does not exist"}
    except Group.DoesNotExist:
        return {"status": "error", "message": "Group does not exist"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Record transaction
def record_transaction(from_user_id, to_user_id, amount, description):
    try:
        from_user = User.objects.get(user_id=from_user_id)
        to_user = User.objects.get(user_id=to_user_id)
        transaction = Transaction.objects.create(
            transaction_id=f"{from_user_id}-{to_user_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            amount=amount,
            description=description,
            from_user=from_user,
            to_user=to_user
        )
        return {"status": "success", "message": "Transaction recorded successfully", "transaction": transaction}
    except User.DoesNotExist:
        return {"status": "error", "message": "From-user or To-user does not exist"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Send notification
def send_notification(sender_id, receiver_id, message):
    try:
        sender = User.objects.get(user_id=sender_id)
        receiver = User.objects.get(user_id=receiver_id)
        notification = Notification.objects.create(
            notification_id=f"{sender_id}-{receiver_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            sender=sender,
            receiver=receiver,
            message=message
        )
        return {"status": "success", "message": "Notification sent successfully", "notification": notification}
    except User.DoesNotExist:
        return {"status": "error", "message": "Sender or receiver does not exist"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



print(User.objects.all())           # List all users


