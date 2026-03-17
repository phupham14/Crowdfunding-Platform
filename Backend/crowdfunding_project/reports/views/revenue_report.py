from rest_framework.views import APIView
from accounts.permission import IsInvestor
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Báo cáo doanh thu ước tính cho nhà đầu tư
class RevenueReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        # placeholder — backend logic sẽ cập nhật sau
        return Response({
            "estimated_profit": 120000000,
            "profit_rate": 18.5,
        })
