from django.db.models import Sum
from transactions.models import Transaction

def get_user_balance(user):
    def total(t):
        return Transaction.objects.filter(
            user=user,
            type=t
        ).aggregate(s=Sum('amount'))['s'] or 0

    fund_in = total("FUND_IN")
    withdraw = total("WITHDRAW")
    invest = total("INVEST")

    return fund_in - withdraw - invest
