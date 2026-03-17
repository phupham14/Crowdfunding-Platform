from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsInvestor
from projects.models import Project
from transactions.models import Transaction
from transactions.serializers.transaction import TransactionSerializer
from accounts.models.wallet import Wallet

class ProjectInvestmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    @transaction.atomic
    def post(self, request, project_id):
        # 1️⃣ Lock project
        try:
            project = Project.objects.select_for_update().get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Lock wallet
        try:
            wallet = Wallet.objects.select_for_update().get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Validate input
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        # 4️⃣ Business rules
        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount > wallet.balance:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if project.raised + amount > project.funding_target:
            return Response(
                {"error": "Funding target exceeded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5️⃣ Trừ tiền
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])

        # 6️⃣ Tạo transaction
        tx = Transaction.objects.create(
            user=request.user,
            project=project,
            amount=amount,
            type="INVEST",
            status="SUCCESS"
        )

        # 7️⃣ Update raised
        project.raised += amount
        project.save(update_fields=["raised"])

        # 8️⃣ Response
        return Response({
            "message": "Investment successful",
            "data": {
                "transaction_id": tx.id,
                "project_id": project.id,
                "amount": str(amount),
                "wallet_balance": str(wallet.balance),
                "project_raised": str(project.raised),
                "created_at": tx.created_at
            }
        }, status=status.HTTP_201_CREATED)
