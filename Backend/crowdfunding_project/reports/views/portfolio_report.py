from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permission import IsInvestor
from rest_framework.permissions import IsAuthenticated
from transactions.models import Transaction

# Báo cáo danh mục đầu tư cho nhà đầu tư
class PortfolioReportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        # Lấy tất cả giao dịch đầu tư của user
        investments = Transaction.objects.filter(user=request.user, type="INVEST", status="SUCCESS")

        total = sum(i.amount for i in investments)

        return Response({
            "user_id": request.user.id,
            "total_invested": total,
            "investment_count": investments.count(),
            "investments": [
                {
                    "id": i.id,
                    "project_id": i.project.id if i.project else None,
                    "project_name": i.project.name if i.project else None,
                    "amount": i.amount,
                    "created_at": i.created_at
                } for i in investments
            ]
        })
