from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.username

class AssetEntry(models.Model):
    name = models.CharField(max_length=24)
    cost_basis = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    price_at_purchase = models.DecimalField(max_digits=20, decimal_places=10, validators=[MinValueValidator(Decimal('0.0000000000'))])
    quantity = models.DecimalField(max_digits=23, decimal_places=10, validators=[MinValueValidator(Decimal('0.0000000000'))])
    coingecko_id = models.CharField(max_length=24, default='')
    # entry_datetime = models.DateTimeField()

    def __str__(self):
        return self.name