from django.db import models
from django.core.exceptions import ValidationError
from accounts.models.user import User
from projects.models import Project
from accounts.models.wallet import Wallet
from accounts.models.BankAccount import BankAccount

class Transaction(models.Model):

    TYPE_CHOICES = (
        ("FUND_IN", "Fund In"),
        ("FUND_OUT", "Fund Out"),
        ("INVEST", "Invest"),
        ("REFUND", "Refund"),
        ("OWNER_DISBURSE", "Owner Disburse"),
        ("OWNER_REPAY", "Owner Repay"),
        ("INVESTOR_PAYOUT", "Investor Payout"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("STRIPE", "Stripe"),
        ("BANK", "Bank Transfer"),
        ("MOCK", "Mock"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=10, default="VND")

    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="STRIPE")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    description = models.CharField(max_length=255, null=True, blank=True)

    # STRIPE FIELDS (CỰC QUAN TRỌNG)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=255, null=True, blank=True)

    # dùng cho fund-out / bank / đối soát
    external_reference = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        indexes = [
            models.Index(fields=["user", "type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["stripe_payment_intent_id"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.amount}"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0")
