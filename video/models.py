import uuid
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=1000)
    encryptor = models.CharField(max_length=1000, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Video(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class KeyStorage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(unique=True, max_length=1000)
    time_stamp = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_keys',
                                blank=True, null=True)
    activated = models.BooleanField(default=False)
    mac_address = models.CharField(max_length=1000, null=True, blank=True)
    watch_time = models.PositiveIntegerField(blank=True, null=True)
    second_screen = models.BooleanField(default=False)  # allow second screen
    expires_at = models.DateField(null=True, blank=True)
    validity = models.CharField(max_length=1000, null=True, blank=True)
    watermark = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.key


class AppModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.id)
