# transactions/services/transaction_service.py
from transactions.models import Transaction

def create_fund_in_transaction(user, amount):
    return Transaction.objects.create(
        user=user,
        amount=amount,
        type="FUND_IN",
        status="PENDING"
    )

def create_fund_out_transaction(user, amount, bank_account):
    return Transaction.objects.create(
        user=user,
        amount=amount,
        type="FUND_OUT",
        status="PENDING",
        bank_account=bank_account
    )

def create_invest_transaction(user, project, amount):
    return Transaction.objects.create(
        user=user,
        project=project,
        amount=amount,
        type="INVEST",
        payment_method="STRIPE",
        status="PENDING"
    )

# Tạo transaction rút tiền cho chủ dự án khi giải ngân
def create_owner_disburse_transaction(user, project, amount):
    return Transaction.objects.create(
        user=user,
        project=project,
        amount=amount,
        type="OWNER_DISBURSE",
        payment_method="MOCK",
        status="SUCCESS",
    )


def create_owner_repay_transaction(user, project, amount):
    return Transaction.objects.create(
        user=user,
        project=project,
        amount=amount,
        type="OWNER_REPAY",
        payment_method="MOCK",
        status="SUCCESS",
    )


def create_investor_payout_transaction(user, project, amount, description=None):
    return Transaction.objects.create(
        user=user,
        project=project,
        amount=amount,
        type="INVESTOR_PAYOUT",
        payment_method="MOCK",
        status="SUCCESS",
        description=description,
    )

def attach_stripe_intent(transaction, intent_id):
    transaction.stripe_payment_intent_id = intent_id
    transaction.save(update_fields=["stripe_payment_intent_id"])
