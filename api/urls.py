from django.urls import path, include
from .views import (
    StockDataView,
    StockDataDetailView,
    TransactionCreateView,
    TransactionListView,
    TransactionRangeView
)

app_name = "users"

urlpatterns = [
    path("stocks/", StockDataView.as_view(), name="stock_data"),
    path("stocks/<str:ticker>/", StockDataDetailView.as_view(), name="stock_detail_data"),
    path("transactions/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transactions/<int:user_id>/", TransactionListView.as_view(), name="transaction_list_view"),
    path("transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/", TransactionRangeView.as_view(), name="transaction_range_view"),
]
