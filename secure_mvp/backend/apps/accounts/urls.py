from django.urls import path

from .views import CSRFTokenView, CurrentUserView, LoginView, LogoutView, RegisterView, UserListView


urlpatterns = [
    path("csrf/", CSRFTokenView.as_view(), name="csrf-token"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="user-list"),
]
