from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "role",
            "bank_name",
            "bank_account",
            "bank_branch",
            "created_at",
            "updated_at",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "password", "role"]
        extra_kwargs = {
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["role"] = "INVESTOR"
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        attrs["username"] = user.email
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.full_name
        return token
