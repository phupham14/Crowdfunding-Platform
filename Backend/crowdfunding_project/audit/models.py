from django.db import models
from accounts.models.user import User


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    action = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50, null=True, blank=True)
    entity_id = models.BigIntegerField(null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"

    def __str__(self):
        return f"{self.action} - {self.entity_type}({self.entity_id})"
