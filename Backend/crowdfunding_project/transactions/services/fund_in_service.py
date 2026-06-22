# transactions/services/fund_in_service.py
from .transaction_service import create_fund_in_transaction, attach_stripe_intent
from .stripe_service import create_payment_intent

def fund_in(user, amount):
    tx = None

    try:
        tx = create_fund_in_transaction(user, amount)

        intent = create_payment_intent(amount, tx.id, user.id)

        attach_stripe_intent(tx, intent.id)

        return intent.client_secret

    except Exception as e:
        print("FUND_IN ERROR:", str(e)) 
        if tx:
            tx.status = "FAILED"
            tx.save(update_fields=["status"])
        raise e