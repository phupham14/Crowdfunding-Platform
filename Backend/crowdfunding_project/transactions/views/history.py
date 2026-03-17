from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsInvestor
from transactions.models import Transaction
from transactions.serializers.transaction import TransactionSerializer

class TransactionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        tx_type = request.query_params.get("type")

        qs = Transaction.objects.filter(user=request.user)

        if tx_type:
            qs = qs.filter(type=tx_type.upper())

        qs = qs.order_by("-created_at")

        serializer = TransactionSerializer(qs, many=True)

        return Response({
            "count": qs.count(),
            "results": serializer.data
        })
