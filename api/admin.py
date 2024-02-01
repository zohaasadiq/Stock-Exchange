from django.contrib import admin
from .models import StockData, Transactions

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'open_price', 'close_price', 'high', 'low', 'volume', 'timestamp']

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'ticker', 'transaction_type', 'transaction_volume', 'transaction_price', 'timestamp']
