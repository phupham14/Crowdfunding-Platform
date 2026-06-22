from decimal import Decimal, InvalidOperation

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.BankAccount import BankAccount
from accounts.permission import IsInvestor
from transactions.services.fund_out_service import process_fund_out

class FundOutAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request):
        try:
            amount = Decimal(str(request.data.get("amount", "")))
        except (InvalidOperation, TypeError):
            return Response(
                {"error": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {"error": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bank_account = BankAccount.objects.get(
                user=request.user,
                is_default=True,
            )
        except BankAccount.DoesNotExist:
            return Response(
                {"error": "Default bank account not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tx = process_fund_out(
                user=request.user,
                amount=amount,
                bank_account=bank_account,
            )

            return Response(
                {
                    "message": "Fund out processed",
                    "transaction_id": tx.id,
                    "status": tx.status,
                    "amount": str(tx.amount),
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
