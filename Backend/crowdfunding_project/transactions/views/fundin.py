from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from transactions.services.fund_in_service import fund_in
from accounts.permission import IsInvestor


class FundInAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request):
        try:
            amount = int(request.data.get("amount", 0))
        except (TypeError, ValueError):
            return Response(
                {"error": "Amount must be a number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= 0:
            return Response(
                {"error": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client_secret = fund_in(request.user, amount)

            return Response({
                "message": "Payment intent created",
                "clientSecret": client_secret,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("FUND_IN API ERROR:", str(e))

            return Response(
                {"error": "Failed to create payment"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )