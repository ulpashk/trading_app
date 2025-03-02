from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsAdmin, IsTrader, IsSalesRep, IsCustomer
from django.contrib.auth import login, logout


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def get_serializer_context(self):
        """Pass the request to serializer context."""
        return {"request": self.request}


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data  # {'refresh': ..., 'access': ..., 'user': ...}

        # 🔹 Get the actual user from the token
        user = User.objects.get(id=tokens['user']['id'])

        # 🔹 Log out any previous session
        logout(request)

        # 🔹 Log in the new user
        login(request, user)

        # 🔹 Store the new token in Django session
        request.session['access_token'] = tokens['access']
        request.session['refresh_token'] = tokens['refresh']
        request.session['user_id'] = user.id  # Store user ID

        return Response(tokens, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class AdminUserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only admins can use this

    def get_object(self):
        """Retrieve a user by their ID from the URL"""
        user_id = self.kwargs.get("pk")  # Get user ID from the URL
        return get_object_or_404(User, id=user_id)  # Return user or 404 if not found


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Ensures the correct user is retrieved

    def get_serializer_context(self):
        """Pass the request to serializer context."""
        return {"request": self.request}

class TraderDashboardView(generics.GenericAPIView):
    permission_classes = [IsTrader]

    def get(self, request, *args, **kwargs):
        return Response({"message": f"Welcome {request.user.username} to the Trader Dashboard"}, status=status.HTTP_200_OK)


class SalesDashboardView(generics.GenericAPIView):
    permission_classes = [IsSalesRep]

    def get(self, request, *args, **kwargs):
        return Response({"message": f"Welcome {request.user.username} to the Sales Representative Dashboard"}, status=status.HTTP_200_OK)


class CustomerDashboardView(generics.GenericAPIView):
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        return Response({"message": f"Welcome {request.user.username} to the Customer Dashboard"}, status=status.HTTP_200_OK)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # Include user role in token response
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
