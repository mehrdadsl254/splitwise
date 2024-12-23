from django.db import models

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:  # Ensure password is hashed
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    detailed_balance = models.JSONField(default=dict, blank=True)
    balance = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Customize related_name for groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name



# Group Model
class Group(models.Model):
    group_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="groups_involved", through="GroupMembers")
    detailed_balance = models.JSONField(default=dict, blank=True)  # Flexible balance per user
    total_balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


# Through Table for Group Members
class GroupMembers(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.name} in {self.group.name}"


# Expense Model
class Expense(models.Model):
    SPLIT_TYPE_CHOICES = [
        ('EQUAL', 'Equal'),
        ('PERCENTAGE', 'Percentage'),
        ('SHARE', 'Share'),
    ]

    expense_id = models.CharField(max_length=50, primary_key=True)
    amount = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPE_CHOICES, default='EQUAL')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_paid")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    participants = models.ManyToManyField(User, related_name="expenses_shared", through="ExpenseParticipants")

    def __str__(self):
        return f"Expense {self.description} - {self.amount}"


# Through Table for Expense Participants
class ExpenseParticipants(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.FloatField(default=0.0)  # Share for the participant

    def __str__(self):
        return f"{self.user.name} - {self.expense.description}"


# Transaction Model
class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    transaction_id = models.CharField(max_length=50, primary_key=True)
    amount = models.FloatField()
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='PENDING')
    description = models.CharField(max_length=255, blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions_received")

    def __str__(self):
        return f"{self.from_user.name} -> {self.to_user.name} : {self.amount}"


# Notification Model
class Notification(models.Model):
    NOTIFICATION_STATUS = [
        ('UNREAD', 'Unread'),
        ('READ', 'Read'),
    ]

    notification_id = models.CharField(max_length=50, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_received")
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='UNREAD')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification to {self.receiver.name}"


# Telegram Mini App Model
class TelegramMiniApp(models.Model):
    app_id = models.CharField(max_length=50, primary_key=True)
    version = models.CharField(max_length=10)
    users = models.ManyToManyField(User, related_name="telegram_users")
    groups = models.ManyToManyField(Group, related_name="telegram_groups")

    def __str__(self):
        return f"Telegram App v{self.version}"