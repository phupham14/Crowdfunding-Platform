# accounts/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("INVESTOR", "Investor"),
        ("PROJECT_OWNER", "Project Owner"),
        ("ADMIN", "Admin"),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.TextField()
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="INVESTOR")

    bank_name = models.CharField(max_length=120, null=True, blank=True)
    bank_account = models.CharField(max_length=50, null=True, blank=True)
    bank_branch = models.CharField(max_length=120, null=True, blank=True)
 
    is_active = models.BooleanField(default=True) # dùng cho khóa / mở khóa tài khoản
    is_verified = models.BooleanField(default=False) # dùng cho duyệt tài khoản

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]  # các trường bắt buộc khi tạo superuser

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    # ---- Custom methods ----
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.email} ({self.role})"