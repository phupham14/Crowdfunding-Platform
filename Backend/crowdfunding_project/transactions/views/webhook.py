import json as _json

from django.conf import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

import stripe

from accounts.models.wallet import Wallet
from projects.models import Project
from transactions.models import Transaction
from transactions.services.investment_service import finalize_investment
from transactions.services.stripe_service import to_stripe_amount

stripe.api_key = settings.STRIPE_SECRET_KEY


def _get_metadata_value(metadata, key):
    if not metadata:
        return None

    try:
        return metadata[key]
    except (KeyError, TypeError):
        return None


def _verify_payment_intent(tx, intent):
    stripe_amount = intent["amount"]
    stripe_currency = intent["currency"]
    expected_currency = tx.currency.lower()
    expected_amount = to_stripe_amount(tx.amount, tx.currency)

    if stripe_currency != expected_currency:
        print("Invalid currency:", stripe_currency, "expected:", expected_currency)
        return False

    if stripe_amount != expected_amount:
        print("Amount mismatch:", stripe_amount, "expected:", expected_amount)
        return False

    return True


def _handle_fund_in(tx):
    wallet, _ = Wallet.objects.select_for_update().get_or_create(
        user=tx.user,
        defaults={"balance": 0}
    )
    wallet.balance += tx.amount
    wallet.save(update_fields=["balance", "updated_at"])
    print(f"Fund-in success | tx_id={tx.id} | +{tx.amount} {tx.currency}")


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        if not settings.DEBUG:
            return Response({"error": "Invalid signature"}, status=400)
        # In DEBUG mode, fall back to parsing without verification so
        # stripe-cli can work even when STRIPE_WEBHOOK_SECRET doesn't
        # match the CLI's signing secret (e.g. first run in Docker).
        try:
            event = _json.loads(payload)
        except Exception:
            return Response({"error": "Invalid payload"}, status=400)
    except Exception as e:
        print("Webhook error:", str(e))
        return Response({"error": "Invalid payload"}, status=400)

    if event["type"] != "payment_intent.succeeded":
        return Response({"ok": True})

    intent = event["data"]["object"]
    tx_id = _get_metadata_value(getattr(intent, "metadata", None), "transaction_id")

    if not tx_id:
        print("Missing transaction_id in payment intent metadata")
        return Response({"ok": True})

    try:
        with transaction.atomic():
            tx = Transaction.objects.select_for_update().get(id=tx_id)

            if tx.status == "SUCCESS":
                return Response({"ok": True})

            if not _verify_payment_intent(tx, intent):
                return Response({"ok": True})

            if tx.type == "FUND_IN":
                _handle_fund_in(tx)
            elif tx.type == "INVEST":
                try:
                    if not finalize_investment(tx):
                        return Response({"ok": True})
                except ValueError as e:
                    print("Investment finalize error:", str(e))
                    return Response({"ok": True})
            else:
                print("Unhandled transaction type:", tx.type)
                return Response({"ok": True})

            tx.status = "SUCCESS"
            tx.save(update_fields=["status"])

    except Transaction.DoesNotExist:
        print("Transaction not found:", tx_id)
        return Response({"ok": True})
    except Project.DoesNotExist:
        print("Project not found for transaction:", tx_id)
        return Response({"ok": True})
    except Exception as e:
        print("Webhook processing error:", str(e))
        return Response({"error": "Internal error"}, status=500)

    return Response({"ok": True})
