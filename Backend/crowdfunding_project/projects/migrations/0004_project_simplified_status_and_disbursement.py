from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_alter_project_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="is_disbursed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending Approval"),
                    ("REJECTED", "Rejected"),
                    ("OPEN", "Open"),
                    ("FUNDED", "Funded"),
                    ("REPAYING", "Repaying"),
                    ("COMPLETED", "Completed"),
                    ("CANCELLED", "Cancelled"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
