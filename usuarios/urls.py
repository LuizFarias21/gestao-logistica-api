from django.urls import path
from .views import RegisterView, UserListView, UserDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
