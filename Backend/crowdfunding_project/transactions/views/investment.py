from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permission import IsInvestor
from projects.models import Project
from transactions.serializers.transaction import TransactionSerializer
from transactions.services.investment_service import create_investment_payment


class ProjectInvestmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    @transaction.atomic
    def post(self, request, project_id):
        try:
            project = Project.objects.select_for_update().get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        try:
            tx, intent = create_investment_payment(
                user=request.user,
                project=project,
                amount=amount,
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Investment payment intent created",
                "data": {
                    "transaction_id": tx.id,
                    "project_id": project.id,
                    "amount": str(amount),
                    "currency": tx.currency,
                    "status": tx.status,
                    "paymentIntentId": intent.id,
                    "clientSecret": intent.client_secret,
                    "created_at": tx.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )
