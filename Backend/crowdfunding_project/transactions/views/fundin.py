from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsInvestor
from transactions.serializers.transaction import TransactionSerializer
from transactions.models import Transaction
from accounts.models.wallet import Wallet

class FundInAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    @transaction.atomic
    def post(self, request):
        # 1️⃣ Validate input
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Lock wallet
        wallet, _ = Wallet.objects.select_for_update().get_or_create(
            user=request.user,
            defaults={"balance": 0}
        )

        # 3️⃣ Cộng tiền
        wallet.balance += amount
        wallet.save(update_fields=["balance"])

        # 4️⃣ Log transaction
        tx = Transaction.objects.create(
            user=request.user,
            amount=amount,
            type="FUND_IN",
            status="SUCCESS",
            description=serializer.validated_data.get("description", "")
        )

        return Response({
            "message": "Fund in successful",
            "data": {
                "transaction_id": tx.id,
                "amount": str(amount),
                "balance": str(wallet.balance),
                "created_at": tx.created_at
            }
        }, status=status.HTTP_201_CREATED)
