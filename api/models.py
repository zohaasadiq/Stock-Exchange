from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ticker

class Transactions(models.Model):
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    transaction_volume = models.IntegerField()
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_id} - {self.user.username}"
