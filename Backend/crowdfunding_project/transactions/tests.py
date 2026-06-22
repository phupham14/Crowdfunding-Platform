from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.BankAccount import BankAccount
from accounts.models.wallet import Wallet
from projects.models import Project
from transactions.models import Transaction

User = get_user_model()


class WalletAndTransactionTests(APITestCase):
    def setUp(self):
        self.investor = User.objects.create_user(
            email="wallet-investor@example.com",
            password="123456",
            full_name="Wallet Investor",
            role="INVESTOR",
        )
        self.other_investor = User.objects.create_user(
            email="other-wallet-investor@example.com",
            password="123456",
            full_name="Other Investor",
            role="INVESTOR",
        )

    def test_investor_can_view_wallet_balance(self):
        wallet = Wallet.objects.get(user=self.investor)
        wallet.balance = Decimal("250.00")
        wallet.save(update_fields=["balance", "updated_at"])
        self.investor.refresh_from_db()
        self.client.force_authenticate(user=self.investor)

        response = self.client.get("/api/accounts/wallet/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], "250.00")
        self.assertEqual(response.data["currency"], "VND")

    @patch("transactions.services.fund_in_service.create_payment_intent")
    def test_fund_in_creates_pending_transaction(self, mock_payment_intent):
        mock_payment_intent.return_value = SimpleNamespace(
            id="pi_fund_in_123",
            client_secret="fund_in_secret",
        )
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            "/api/transactions/fund-in/",
            {"amount": "500"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["clientSecret"], "fund_in_secret")
        self.assertTrue(
            Transaction.objects.filter(
                user=self.investor,
                amount=Decimal("500.00"),
                type="FUND_IN",
                status="PENDING",
                stripe_payment_intent_id="pi_fund_in_123",
            ).exists()
        )

    def test_fund_out_requires_default_bank_account(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            "/api/transactions/fund-out/",
            {"amount": "100"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Default bank account not found")

    def test_fund_out_debits_wallet_and_creates_success_transaction(self):
        wallet = Wallet.objects.get(user=self.investor)
        wallet.balance = Decimal("300.00")
        wallet.save(update_fields=["balance", "updated_at"])
        bank_account = BankAccount.objects.create(
            user=self.investor,
            bank_name="VCB",
            account_number="123456789",
            account_holder="Wallet Investor",
            is_default=True,
        )
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            "/api/transactions/fund-out/",
            {"amount": "120"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "SUCCESS")

        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, Decimal("180.00"))
        self.assertTrue(
            Transaction.objects.filter(
                user=self.investor,
                amount=Decimal("120.00"),
                type="FUND_OUT",
                status="SUCCESS",
                bank_account=bank_account,
            ).exists()
        )

    def test_transaction_history_only_returns_authenticated_user_transactions(self):
        Transaction.objects.create(
            user=self.investor,
            amount=Decimal("100.00"),
            type="FUND_IN",
            payment_method="MOCK",
            status="SUCCESS",
        )
        Transaction.objects.create(
            user=self.investor,
            amount=Decimal("50.00"),
            type="INVEST",
            payment_method="MOCK",
            status="SUCCESS",
        )
        Transaction.objects.create(
            user=self.other_investor,
            amount=Decimal("999.00"),
            type="FUND_IN",
            payment_method="MOCK",
            status="SUCCESS",
        )
        self.client.force_authenticate(user=self.investor)

        response = self.client.get("/api/transactions/history/?type=fund_in")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["type"], "FUND_IN")
        self.assertEqual(response.data["results"][0]["amount"], "100.00")


class InvestmentPaymentTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner-investment@example.com",
            password="123456",
            full_name="Owner",
            role="PROJECT_OWNER",
        )
        self.investor = User.objects.create_user(
            email="investor-investment@example.com",
            password="123456",
            full_name="Investor",
            role="INVESTOR",
        )
        self.project = Project.objects.create(
            owner=self.owner,
            name="Community Solar",
            category="Energy",
            funding_target=Decimal("1000.00"),
            raised=Decimal("100.00"),
            status="OPEN",
        )

    @patch("transactions.services.investment_service.create_payment_intent")
    def test_investor_can_create_investment_payment_intent(self, mock_payment_intent):
        mock_payment_intent.return_value = SimpleNamespace(
            id="pi_test_123",
            client_secret="pi_test_secret",
        )
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            f"/api/transactions/projects/{self.project.id}/invest/",
            {"amount": "200.00", "type": "INVEST"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["status"], "PENDING")
        self.assertEqual(response.data["data"]["paymentIntentId"], "pi_test_123")
        self.assertTrue(
            Transaction.objects.filter(
                user=self.investor,
                project=self.project,
                amount=Decimal("200.00"),
                type="INVEST",
                status="PENDING",
                stripe_payment_intent_id="pi_test_123",
            ).exists()
        )

        self.project.refresh_from_db()
        self.assertEqual(self.project.raised, Decimal("100.00"))

    def test_investment_rejects_amount_exceeding_remaining_target(self):
        self.client.force_authenticate(user=self.investor)

        response = self.client.post(
            f"/api/transactions/projects/{self.project.id}/invest/",
            {"amount": "1000.00", "type": "INVEST"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Funding target exceeded",
        )
        self.assertFalse(
            Transaction.objects.filter(user=self.investor, project=self.project).exists()
        )


class ProjectOwnerCashflowTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="123456",
            full_name="Owner",
            role="PROJECT_OWNER",
        )
        self.investor_a = User.objects.create_user(
            email="a@example.com",
            password="123456",
            full_name="Investor A",
            role="INVESTOR",
        )
        self.investor_b = User.objects.create_user(
            email="b@example.com",
            password="123456",
            full_name="Investor B",
            role="INVESTOR",
        )

        self.project = Project.objects.create(
            owner=self.owner,
            name="Factory Expansion",
            category="Business",
            funding_target=Decimal("100.00"),
            raised=Decimal("100.00"),
            status="FUNDED",
        )

        Transaction.objects.create(
            user=self.investor_a,
            project=self.project,
            amount=Decimal("60.00"),
            type="INVEST",
            payment_method="MOCK",
            status="SUCCESS",
        )
        Transaction.objects.create(
            user=self.investor_b,
            project=self.project,
            amount=Decimal("40.00"),
            type="INVEST",
            payment_method="MOCK",
            status="SUCCESS",
        )

    def test_owner_can_disburse_project_funds(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(f"/api/transactions/projects/{self.project.id}/disburse/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        owner_wallet = Wallet.objects.get(user=self.owner)

        self.assertTrue(self.project.is_disbursed)
        self.assertEqual(owner_wallet.balance, Decimal("100.00"))
        self.assertTrue(
            Transaction.objects.filter(
                user=self.owner,
                project=self.project,
                type="OWNER_DISBURSE",
                status="SUCCESS",
            ).exists()
        )

    def test_owner_repayment_is_split_by_investment_ratio(self):
        self.project.is_disbursed = True
        self.project.save(update_fields=["is_disbursed"])

        owner_wallet = Wallet.objects.get(user=self.owner)
        owner_wallet.balance = Decimal("100.00")
        owner_wallet.save(update_fields=["balance", "updated_at"])

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"/api/transactions/projects/{self.project.id}/repay/",
            {"amount": "50.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        owner_wallet.refresh_from_db()
        wallet_a = Wallet.objects.get(user=self.investor_a)
        wallet_b = Wallet.objects.get(user=self.investor_b)

        self.assertEqual(self.project.status, "REPAYING")
        self.assertEqual(self.project.total_repaid, Decimal("50.00"))
        self.assertEqual(owner_wallet.balance, Decimal("50.00"))
        self.assertEqual(wallet_a.balance, Decimal("30.00"))
        self.assertEqual(wallet_b.balance, Decimal("20.00"))
        self.assertEqual(
            Transaction.objects.filter(
                project=self.project,
                type="INVESTOR_PAYOUT",
                status="SUCCESS",
            ).count(),
            2,
        )

    def test_project_is_completed_after_full_repayment(self):
        self.project.is_disbursed = True
        self.project.save(update_fields=["is_disbursed"])

        owner_wallet = Wallet.objects.get(user=self.owner)
        owner_wallet.balance = Decimal("100.00")
        owner_wallet.save(update_fields=["balance", "updated_at"])

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"/api/transactions/projects/{self.project.id}/repay/",
            {"amount": "100.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "COMPLETED")
        self.assertEqual(self.project.total_repaid, Decimal("100.00"))
