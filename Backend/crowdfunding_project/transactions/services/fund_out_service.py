# fund_out_service.py
from django.db import transaction as db_transaction
from .wallet_service import debit_wallet, credit_wallet
from .transaction_service import create_fund_out_transaction

def process_fund_out(user, amount, bank_account):

    with db_transaction.atomic():

        # 1. tạo transaction
        tx = create_fund_out_transaction(user, amount, bank_account)

        # 2. trừ tiền
        debit_wallet(user, amount)

    # 3. gọi payout (mock)
    success = simulate_bank_transfer(tx)

    # 4. xử lý kết quả
    if success:
        tx.status = "SUCCESS"
        tx.save(update_fields=["status", "updated_at"])
    else:
        # rollback tiền
        credit_wallet(user, amount)

        tx.status = "FAILED"
        tx.save(update_fields=["status", "updated_at"])

    return tx


def simulate_bank_transfer(transaction):
    """
    MOCK: sau này thay bằng bank API
    """
    return True  # hoặc random True/False để test