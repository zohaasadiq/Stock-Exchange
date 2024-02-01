# views.py
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from rest_framework import status
from users.models import NewUser
from .models import StockData, Transactions
from .serializers import StockDataSerializer, TransactionsSerializer
import datetime

class StockDataView(APIView):
    def post(self, request):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        cache_key = 'stock_data'
        data = cache.get(cache_key)
        if not data:
            stocks = StockData.objects.all()
            serializer = StockDataSerializer(stocks, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*60*24)
        return Response(data)

class StockDataDetailView(APIView):
    def get(self, request, ticker):
        cache_key = f'stock_data_{ticker}'
        data = cache.get(cache_key)
        if not data:
            stocks = StockData.objects.filter(ticker=ticker)
            serializer = StockDataSerializer(stocks, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*60*24)
        return Response(data)

class TransactionCreateView(APIView):
    def post(self, request):
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user')
            ticker = serializer.validated_data.get('ticker')
            transaction_type = serializer.validated_data.get('transaction_type')
            transaction_volume = serializer.validated_data.get('transaction_volume')

            user = get_object_or_404(NewUser, pk=user_id)
            stock = get_object_or_404(StockData, ticker=ticker)

            # Assuming 'open_price' as current price
            transaction_price = stock.open_price * transaction_volume

            # Update user balance
            if transaction_type == 'buy':
                if user.balance < transaction_price:
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
                user.balance -= transaction_price
            elif transaction_type == 'sell':
                user.balance += transaction_price
            else:
                return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

            user.save()

            # Create Transaction
            Transactions.objects.create(
                user=user,
                ticker=ticker,
                transaction_type=transaction_type,
                transaction_volume=transaction_volume,
                transaction_price=transaction_price,
                timestamp=datetime.now()
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):
    def get(self, request, user_id):
        transactions = Transactions.objects.filter(user_id=user_id).order_by('-timestamp')
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)


class TransactionRangeView(APIView):
    def get(self, request, user_id, start_timestamp, end_timestamp,):
        start = parse_datetime(start_timestamp)
        end = parse_datetime(end_timestamp)
        transactions = Transactions.objects.filter(
            user_id=user_id, 
            timestamp__gte=start, 
            timestamp__lte=end
        ).order_by('-timestamp')
        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)
