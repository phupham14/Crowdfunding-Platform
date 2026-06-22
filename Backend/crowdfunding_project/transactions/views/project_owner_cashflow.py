from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permission import IsProjectOwner
from projects.models import Project
from transactions.serializers.transaction import TransactionSerializer
from transactions.services.project_owner_cashflow_service import (
    disburse_project_funds,
    repay_project_investors,
)


class ProjectDisbursementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def post(self, request, project_id):
        try:
            project, tx = disburse_project_funds(request.user, project_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "message": "Project funds disbursed",
                "project_id": project.id,
                "status": project.status,
                "is_disbursed": project.is_disbursed,
                "transaction": TransactionSerializer(tx).data,
            },
            status=status.HTTP_200_OK,
        )


class ProjectRepaymentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def post(self, request, project_id):
        amount = request.data.get("amount")

        if amount is None:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project, tx, payouts = repay_project_investors(request.user, project_id, amount)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "message": "Repayment processed",
                "project_id": project.id,
                "status": project.status,
                "total_repaid": str(project.total_repaid),
                "repayment_transaction": TransactionSerializer(tx).data,
                "payout_count": len(payouts),
            },
            status=status.HTTP_200_OK,
        )
