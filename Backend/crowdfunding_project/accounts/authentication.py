from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models.user import User

class CustomJWTAuth(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed({
                "detail": "User not found",
                "code": "user_not_found"
            })
