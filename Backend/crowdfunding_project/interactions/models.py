from django.db import models

class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ("view", "View"),
        ("click", "Click"),
        ("save", "Save"),
        ("invest", "Invest"),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)

    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)

    # optional nhưng rất hữu ích cho ML
    value = models.FloatField(default=1.0)

    # context (rất quan trọng cho recommender)
    source = models.CharField(max_length=50, null=True, blank=True)  
    # homepage / search / recommendation

    session_id = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_interactions"
        indexes = [
            models.Index(fields=["user", "project"]),
            models.Index(fields=["interaction_type"]),
            models.Index(fields=["created_at"]),
        ]
