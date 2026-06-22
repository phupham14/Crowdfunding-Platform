from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_project_simplified_status_and_disbursement"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="total_repaid",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
