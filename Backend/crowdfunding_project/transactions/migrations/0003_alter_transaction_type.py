from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_remove_transaction_bank_reference_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="type",
            field=models.CharField(
                choices=[
                    ("FUND_IN", "Fund In"),
                    ("FUND_OUT", "Fund Out"),
                    ("INVEST", "Invest"),
                    ("REFUND", "Refund"),
                    ("OWNER_DISBURSE", "Owner Disburse"),
                    ("OWNER_REPAY", "Owner Repay"),
                    ("INVESTOR_PAYOUT", "Investor Payout"),
                ],
                max_length=30,
            ),
        ),
    ]
