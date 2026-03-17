# projects/models.py
from django.db import models
from accounts.models.user import User


class Project(models.Model):

    STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("CANCELLED", "Cancelled"),
        ("REJECTED", "Rejected"),
        ("PENDING", "Pending Approval"),
    )

    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    funding_target = models.DecimalField(max_digits=18, decimal_places=2)
    raised = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    apr_expected = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    risk_level = models.SmallIntegerField(null=True, blank=True)
    expected_return_score = models.SmallIntegerField(null=True, blank=True)
    liquidity_score = models.SmallIntegerField(null=True, blank=True)

    min_invest_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    max_invest_amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    min_invest_duration_months = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name
    
class AIRecommendation(models.Model):
    SOURCE_CHOICES = (
        ("RULE", "Rule Engine"),
        ("OPENAI", "OpenAI"),
        ("LOCAL_MODEL", "Local ML Model"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    projects_json = models.JSONField()
    generated_by = models.CharField(max_length=20, choices=SOURCE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_recommendations"