from interactions.models import UserInteraction
from projects.models import Project
from accounts.models.wallet import Wallet
from transactions.models import Transaction

from .stripe_service import create_payment_intent
from .transaction_service import attach_stripe_intent, create_invest_transaction


def validate_investment(project, amount):
    if project.status != "OPEN":
        raise ValueError("Only open projects can receive investments")

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if project.raised + amount > project.funding_target:
        raise ValueError("Funding target exceeded")

    if project.max_invest_amount and amount > project.max_invest_amount:
        raise ValueError("Amount exceeds max investment amount")

    # if amount < project.min_invest_amount:
    #     raise ValueError("Amount is below min investment amount")


def create_investment_payment(user, project, amount):
    tx = None

    try:
        validate_investment(project, amount)

        tx = create_invest_transaction(
            user=user,
            project=project,
            amount=amount,
        )

        intent = create_payment_intent(
            amount=amount,
            transaction_id=tx.id,
            user_id=user.id,
            currency=tx.currency,
            metadata={
                "project_id": str(project.id),
                "transaction_type": tx.type,
            },
        )
        attach_stripe_intent(tx, intent.id)

        return tx, intent
    except Exception:
        if tx:
            tx.status = "FAILED"
            tx.save(update_fields=["status"])
        raise


def finalize_investment(tx):
    if not tx.project_id:
        print("Invest transaction missing project:", tx.id)
        return False

    project = Project.objects.select_for_update().get(id=tx.project_id)
    validate_investment(project, tx.amount)

    project.raised += tx.amount
    if project.raised >= project.funding_target:
        project.status = "FUNDED"
        project.save(update_fields=["raised", "status", "updated_at"])
    else:
        project.save(update_fields=["raised", "updated_at"])

    balance = Wallet.objects.select_for_update().get(user=tx.user)
    if balance.balance < tx.amount:
        print(f"Insufficient balance for investment | tx_id={tx.id} | user_id={tx.user.id}")
        return False
    balance.balance -= tx.amount
    balance.save(update_fields=["balance", "updated_at"])

    UserInteraction.objects.get_or_create(
        user=tx.user,
        project=project,
        interaction_type="invest",
        defaults={"value": 5},
    )
    print(
        f"Investment success | tx_id={tx.id} | project_id={project.id} | +{tx.amount} {tx.currency}"
    )
    return True
