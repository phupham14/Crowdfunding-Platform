# transactions/services/stripe_service.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

ZERO_DECIMAL_CURRENCIES = {"vnd"}


def to_stripe_amount(amount, currency="vnd"):
    currency = currency.lower()
    numeric_amount = int(amount)

    if currency in ZERO_DECIMAL_CURRENCIES:
        return numeric_amount

    return numeric_amount * 100


def create_payment_intent(amount, transaction_id, user_id, currency="vnd", metadata=None):
    metadata = {
        "transaction_id": str(transaction_id),
        "user_id": str(user_id),
        **(metadata or {})
    }

    intent = stripe.PaymentIntent.create(
        amount=to_stripe_amount(amount, currency),
        currency=currency.lower(),
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never"
        },
        metadata=metadata
    )
    return intent
