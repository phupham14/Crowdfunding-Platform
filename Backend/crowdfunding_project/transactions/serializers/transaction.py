from rest_framework import serializers
from ..models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["user", "status", "created_at", "updated_at"]
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0"
            )
        return value