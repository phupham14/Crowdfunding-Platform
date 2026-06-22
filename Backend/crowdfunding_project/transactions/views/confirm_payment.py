from django.conf import settings
from django.db import transaction as db_transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import stripe

from transactions.models import Transaction
from transactions.views.webhook import _handle_fund_in, _get_metadata_value
from transactions.services.investment_service import finalize_investment

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    payment_intent_id = request.data.get("paymentIntentId")
    if not payment_intent_id:
        return Response({"error": "Missing paymentIntentId"}, status=400)

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)

    if intent.status != "succeeded":
        return Response({"error": f"Payment not succeeded: {intent.status}"}, status=400)

    tx_id = _get_metadata_value(intent.metadata, "transaction_id")
    user_id = _get_metadata_value(intent.metadata, "user_id")

    if not tx_id:
        return Response({"error": "Invalid payment intent"}, status=400)

    if str(request.user.id) != str(user_id):
        return Response({"error": "Unauthorized"}, status=403)

    try:
        with db_transaction.atomic():
            tx = Transaction.objects.select_for_update().get(
                id=tx_id, user=request.user
            )

            if tx.status == "SUCCESS":
                return Response({"ok": True})

            if tx.type == "FUND_IN":
                _handle_fund_in(tx)
            elif tx.type == "INVEST":
                if not finalize_investment(tx):
                    return Response({"error": "Investment processing failed"}, status=400)
            else:
                return Response({"error": "Unhandled transaction type"}, status=400)

            tx.status = "SUCCESS"
            tx.save(update_fields=["status"])

    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)
    except Exception as e:
        print("Confirm payment error:", str(e))
        return Response({"error": "Internal error"}, status=500)

    return Response({"ok": True})
