from django.conf import settings
from django.db import models

class BankAccount(models.Model):

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    bank_name = models.CharField(max_length=120)
    account_number = models.CharField(max_length=50)
    account_holder = models.CharField(max_length=120)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bank_accounts"

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"