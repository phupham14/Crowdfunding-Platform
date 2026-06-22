from decimal import Decimal, ROUND_DOWN

from django.db import transaction as db_transaction

from accounts.models.wallet import Wallet
from projects.models import Project
from transactions.models import Transaction
from transactions.services.transaction_service import (
    create_investor_payout_transaction,
    create_owner_disburse_transaction,
    create_owner_repay_transaction,
)


def disburse_project_funds(owner, project_id):
    with db_transaction.atomic():
        project = Project.objects.select_for_update().get(id=project_id, owner=owner)

        if project.status != "FUNDED":
            raise ValueError("Project must be FUNDED before disbursement")
        if project.is_disbursed:
            raise ValueError("Project funds have already been disbursed")

        owner_wallet = Wallet.objects.select_for_update().get(user=owner)
        owner_wallet.balance += project.raised
        owner_wallet.save(update_fields=["balance", "updated_at"])

        tx = create_owner_disburse_transaction(owner, project, project.raised)

        project.is_disbursed = True
        project.save(update_fields=["is_disbursed", "updated_at"])

        return project, tx


def repay_project_investors(owner, project_id, amount):
    amount = Decimal(str(amount))

    with db_transaction.atomic():
        project = Project.objects.select_for_update().get(id=project_id, owner=owner)

        if not project.is_disbursed:
            raise ValueError("Project has not been disbursed")
        if project.status not in ["FUNDED", "REPAYING"]:
            raise ValueError("Project is not in a repayable state")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        remaining = project.raised - project.total_repaid
        if remaining <= 0:
            raise ValueError("Project has already been fully repaid")
        if amount > remaining:
            raise ValueError("Repayment amount exceeds remaining project balance")

        owner_wallet = Wallet.objects.select_for_update().get(user=owner)
        if owner_wallet.balance < amount:
            raise ValueError("Insufficient balance")

        investments = list(
            Transaction.objects.filter(
                project=project,
                type="INVEST",
                status="SUCCESS",
            ).select_related("user")
        )
        total_invested = sum((tx.amount for tx in investments), Decimal("0"))
        if total_invested <= 0:
            raise ValueError("No successful investments found for this project")

        owner_wallet.balance -= amount
        owner_wallet.save(update_fields=["balance", "updated_at"])

        owner_tx = create_owner_repay_transaction(owner, project, amount)

        payouts = []
        distributed = Decimal("0")
        for index, investment in enumerate(investments):
            if index == len(investments) - 1:
                payout_amount = amount - distributed
            else:
                ratio = investment.amount / total_invested
                payout_amount = (amount * ratio).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
                distributed += payout_amount

            investor_wallet = Wallet.objects.select_for_update().get(user=investment.user)
            investor_wallet.balance += payout_amount
            investor_wallet.save(update_fields=["balance", "updated_at"])

            payouts.append(
                create_investor_payout_transaction(
                    investment.user,
                    project,
                    payout_amount,
                    description=f"Payout from owner repayment for project {project.id}",
                )
            )

        project.total_repaid += amount
        if project.total_repaid >= project.raised:
            project.status = "COMPLETED"
        else:
            project.status = "REPAYING"
        project.save(update_fields=["total_repaid", "status", "updated_at"])

        return project, owner_tx, payouts
