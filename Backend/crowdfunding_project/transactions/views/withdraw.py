from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsInvestor
from transactions.serializers.transaction import TransactionSerializer
from transactions.models import Transaction
from accounts.models.wallet import Wallet

class WithdrawAPIView(APIView):
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
        try:
            wallet = Wallet.objects.select_for_update().get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Check balance
        if amount > wallet.balance:
            return Response(
                {
                    "error": "Insufficient balance",
                    "current_balance": str(wallet.balance)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Trừ tiền
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])

        # 5️⃣ Log transaction
        tx = Transaction.objects.create(
            user=request.user,
            amount=amount,
            type="WITHDRAW",
            status="SUCCESS",
            description=serializer.validated_data.get("description", "")
        )

        return Response({
            "message": "Withdraw successful",
            "data": {
                "transaction_id": tx.id,
                "amount": str(amount),
                "balance": str(wallet.balance),
                "created_at": tx.created_at
            }
        }, status=status.HTTP_201_CREATED)
