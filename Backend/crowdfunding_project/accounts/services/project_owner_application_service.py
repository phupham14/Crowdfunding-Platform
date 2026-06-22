from django.utils import timezone
from rest_framework.exceptions import ValidationError

from accounts.models.project_owner_application import ProjectOwnerApplication


def submit_project_owner_application(user, validated_data):
    if user.role == "PROJECT_OWNER":
        raise ValidationError({"detail": "User is already a project owner"})

    application, created = ProjectOwnerApplication.objects.get_or_create(
        user=user,
        defaults={**validated_data, "status": "PENDING"},
    )

    if created:
        return application, created

    if application.status == "APPROVED":
        raise ValidationError({"detail": "Application has already been approved"})

    for field, value in validated_data.items():
        setattr(application, field, value)

    application.status = "PENDING"
    application.reject_reason = None
    application.reviewed_by = None
    application.reviewed_at = None
    application.save()
    return application, created


def approve_project_owner_application(application, reviewer):
    if application.status == "APPROVED":
        raise ValidationError({"detail": "Application has already been approved"})

    application.status = "APPROVED"
    application.reject_reason = None
    application.reviewed_by = reviewer
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reject_reason", "reviewed_by", "reviewed_at", "updated_at"])

    user = application.user
    user.role = "PROJECT_OWNER"
    user.save(update_fields=["role", "updated_at"])
    return application


def reject_project_owner_application(application, reviewer, reject_reason):
    # if application.status == "APPROVED":
    #     raise ValidationError({"detail": "Approved application cannot be rejected"})

    application.status = "REJECTED"
    application.reject_reason = reject_reason
    application.reviewed_by = reviewer
    application.reviewed_at = timezone.now()

    user = application.user
    user.role = "INVESTOR"
    
    user.save(update_fields=["role", "updated_at"])
    application.save(update_fields=["status", "reject_reason", "reviewed_by", "reviewed_at", "updated_at"])
    return application
