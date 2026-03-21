import logging

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.throttling import LoginRateThrottle, RegisterRateThrottle, SensitiveActionRateThrottle

from .models import User
from .permissions import IsAdminRole
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from .services import login_user, logout_user, register_user


auth_logger = logging.getLogger("apps.auth")


@method_decorator(csrf_protect, name="dispatch")
class CSRFTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data["email"])
        register_user(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            auth_logger.warning("auth.login_failed ip=%s", request.META.get("REMOTE_ADDR", "unknown"))
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        login_user(request, user)
        return Response(UserSerializer(user).data)


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    throttle_classes = [SensitiveActionRateThrottle]

    def post(self, request):
        logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.order_by("email")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    search_fields = ("email", "username", "first_name", "last_name")
