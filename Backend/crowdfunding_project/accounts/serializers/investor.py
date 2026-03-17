from rest_framework import serializers
from accounts.models.user import User

class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "phone"]
        extra_kwargs = {
            "full_name": {"required": False},
            "phone": {"required": False},
        }
