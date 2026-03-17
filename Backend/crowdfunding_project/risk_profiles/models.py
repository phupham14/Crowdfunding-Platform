# risk_profiles/models.py
from django.db import models
from accounts.models.user import User

class RiskProfile(models.Model):

    RISK_TIER_CHOICES = (
        ("CONSERVATIVE", "Conservative"),
        ("BALANCED", "Balanced"),
        ("AGGRESSIVE", "Aggressive"),
    )

    id = models.BigAutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="risk_profile"
    )

    age = models.IntegerField(null=True, blank=True) 
    income = models.BigIntegerField(null=True, blank=True)
    investment_experience = models.IntegerField(null=True, blank=True)
    risk_tolerance = models.IntegerField(null=True, blank=True) 

    base_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    risk_tier = models.CharField(
        max_length=20,
        choices=RISK_TIER_CHOICES,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "risk_profiles"
