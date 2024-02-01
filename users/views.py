from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from .models import NewUser

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            if newuser := reg_serializer.save():
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):
    def get(self, request, username):
        cache_key = f"user_data_{username}"
        cache_time = 86400
        user_data = cache.get(cache_key)
        if not user_data:
            try:
                user = NewUser.objects.get(username=username)
                serializer = RegisterUserSerializer(user)
                user_data = serializer.data
                cache.set(cache_key, user_data, cache_time)
            except NewUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_data, status=status.HTTP_200_OK)