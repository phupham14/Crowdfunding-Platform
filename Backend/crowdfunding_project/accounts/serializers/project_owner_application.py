from rest_framework import serializers

from accounts.models.project_owner_application import ProjectOwnerApplication


class ProjectOwnerApplicationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    reviewer_email = serializers.EmailField(source="reviewed_by.email", read_only=True)

    class Meta:
        model = ProjectOwnerApplication
        fields = [
            "id",
            "user_id",
            "user_email",
            "user_full_name",
            "business_name",
            "business_type",
            "tax_code",
            "id_number",
            "bio",
            "experience",
            "document_url",
            "status",
            "reject_reason",
            "reviewer_email",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "user_email",
            "user_full_name",
            "status",
            "reject_reason",
            "reviewer_email",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]


class ProjectOwnerApplicationReviewSerializer(serializers.Serializer):
    reject_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        action = self.context.get("action")
        reject_reason = attrs.get("reject_reason", "").strip()

        if action == "reject" and not reject_reason:
            raise serializers.ValidationError({"reject_reason": "Reject reason is required"})

        attrs["reject_reason"] = reject_reason
        return attrs
