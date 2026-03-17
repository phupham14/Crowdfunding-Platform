# transactions/models.py
from django.db import models
from accounts.models.user import User
from projects.models import Project
from django.core.exceptions import ValidationError


class Transaction(models.Model):
    TYPE_CHOICES = (
        ("FUND_IN", "Fund In"), # Nạp tiền
        ("INVEST", "Invest"), # Đầu tư
        ("REFUND", "Refund"), # Hoàn tiền
        ("WITHDRAW", "Withdraw"), # Rút tiền
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=10, default="VND")

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255, null=True, blank=True)
    bank_reference = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.amount}"
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0")
