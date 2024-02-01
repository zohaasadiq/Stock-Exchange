from django.urls import path, include
from .views import CustomUserCreate, UserDataView

app_name = "users"

urlpatterns = [
    path("", CustomUserCreate.as_view(), name="create_user"),
    path("<str:username>/", UserDataView.as_view(), name="get_user"),
]
