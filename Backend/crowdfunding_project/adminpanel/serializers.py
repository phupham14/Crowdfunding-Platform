from rest_framework import serializers
from accounts.serializers.users import UserSerializer
from projects.serializers.project import ProjectSerializer
from transactions.serializers.transaction import TransactionSerializer
from transactions.models import Transaction
from accounts.models.user import User
from projects.models import Project
from django.contrib.auth.hashers import make_password

# serializer tổng hợp nếu cần dashboard
class AdminDashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_projects = serializers.IntegerField()
    total_transactions = serializers.IntegerField()
    total_invest_amount = serializers.DecimalField(max_digits=18, decimal_places=2)

class AdminUserSerializer(serializers.ModelSerializer):
    locked = serializers.SerializerMethodField()

    class Meta: 
        model = User
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def get_locked(self, obj):
        return not obj.is_active

class AdminProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class AdminTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "password", "role", "phone"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_role(self, value):
        if value != "ADMIN":
            raise serializers.ValidationError("Role must be ADMIN")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
