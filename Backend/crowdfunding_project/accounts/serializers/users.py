from rest_framework import serializers
from ..models.user import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

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
            "updated_at"
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "password", "role"]

    def create(self, validated_data):
        # hash password trước khi lưu
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    # Ghi đè validate để login bằng email
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)  # mặc định authenticate dùng username
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        # gán user vào attrs để super validate tạo token
        attrs["username"] = user.email  
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Thêm thông tin vào token nếu muốn
        token['role'] = user.role
        token['full_name'] = user.full_name
        return token