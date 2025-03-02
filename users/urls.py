from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('admin/user/<int:pk>/', AdminUserUpdateView.as_view(), name='admin-update-user'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('traderdash/', TraderDashboardView.as_view(), name='trader-dashboard'),
    path('salesdash/', SalesDashboardView.as_view(), name='sales-dashboard'),
    path('customerdash/', CustomerDashboardView.as_view(), name='customer-dashboard'),
]