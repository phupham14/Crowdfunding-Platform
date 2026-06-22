# wallet_service.py
from django.db import transaction as db_transaction
from accounts.models.wallet import Wallet

def debit_wallet(user, amount):
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)

        if wallet.balance < amount:
            raise ValueError("Insufficient balance")

        wallet.balance -= amount
        wallet.save(update_fields=["balance"])

        wallet.updated_at = wallet.updated_at  # Trigger auto_now update
        wallet.save(update_fields=["updated_at"])

        return wallet

def credit_wallet(user, amount):
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)

        wallet.balance += amount
        wallet.save(update_fields=["balance"])

        wallet.updated_at = wallet.updated_at  # Trigger auto_now update
        wallet.save(update_fields=["updated_at"])

        return wallet