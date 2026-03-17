from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from transactions.models import Transaction
from threading import Thread

User = get_user_model()


class WithdrawTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("withdraw")  # url name của WithdrawAPIView

        # Nạp tiền 1000 cho user
        Transaction.objects.create(user=self.user, amount=1000, type="FUND_IN")

    def test_withdraw_equal_balance(self):
        response = self.client.post(self.url, {
            "amount": 1000,
            "description": "Withdraw full",
            "type": "WITHDRAW"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # balance phải = 0
        balance = self._get_balance()
        self.assertEqual(balance, 0)

    def _get_balance(self):
        fund_in = Transaction.objects.filter(user=self.user, type="FUND_IN").aggregate(total_amount=('amount'))['total_amount'] or 0
        withdraw = Transaction.objects.filter(user=self.user, type="WITHDRAW").aggregate(total_amount=('amount'))['total_amount'] or 0
        invest = Transaction.objects.filter(user=self.user, type="INVEST").aggregate(total_amount=('amount'))['total_amount'] or 0
        return fund_in - withdraw - invest

    def test_withdraw_greater_than_balance(self):
        response = self.client.post(self.url, {
            "amount": 1500,
            "description": "Too much withdraw",
            "type": "WITHDRAW"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient balance", response.data["message"])

    def test_concurrent_withdraw(self):
        """
        Kiểm tra 2 request withdraw cùng lúc,
        tổng amount > balance, chỉ 1 request thành công
        """

        responses = []

        def withdraw(amount):
            resp = self.client.post(self.url, {
                "amount": amount,
                "description": "Concurrent",
                "type": "WITHDRAW"
            }, format="json")
            responses.append(resp)

        # Hai thread withdraw 700 + 700 = 1400, balance = 1000
        t1 = Thread(target=withdraw, args=(700,))
        t2 = Thread(target=withdraw, args=(700,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Chỉ 1 request thành công
        success_count = sum(1 for r in responses if r.status_code == status.HTTP_201_CREATED)
        fail_count = sum(1 for r in responses if r.status_code == status.HTTP_400_BAD_REQUEST)

        self.assertEqual(success_count, 1)
        self.assertEqual(fail_count, 1)

        # balance còn lại = 300
        balance = self._get_balance()
        self.assertEqual(balance, 300)
