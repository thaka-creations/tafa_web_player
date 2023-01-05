import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import manager

# Create your models here.
ACCOUNT_STATUS = [
    ("REGISTRATION", "REGISTRATION"),
    ("ACTIVE", "ACTIVE"),
    ("DEACTIVATED", "DEACTIVATED"),
    ("SUSPENDED", "SUSPENDED"),
]


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    account_status = models.CharField(max_length=255, choices=ACCOUNT_STATUS, default="REGISTRATION")

    USERNAME_FIELD = "username"

    objects = manager.UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        ordering = ["-date_created"]


class PublicUser(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="public_user")
    school = models.CharField(max_length=1000, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    profile_status = models.CharField(max_length=255, choices=ACCOUNT_STATUS, default="REGISTRATION")


class Staff(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_user")
    profile_status = models.CharField(max_length=255, choices=ACCOUNT_STATUS, default="ACTIVE")
