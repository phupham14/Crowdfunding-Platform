from django.db import models


class ProjectOwnerApplication(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="project_owner_application",
    )
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100, null=True, blank=True)
    tax_code = models.CharField(max_length=50, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    document_url = models.URLField(max_length=500, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    reject_reason = models.TextField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_project_owner_applications",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project_owner_applications"

    def __str__(self):
        return f"{self.user.email} - {self.status}"
