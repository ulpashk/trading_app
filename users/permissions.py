from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow access only to Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrader(BasePermission):
    """Allow access only to Trader users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trader'

class IsSalesRep(BasePermission):
    """Allow access only to Sales Representatives"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales'

class IsCustomer(BasePermission):
    """Allow access only to Customers"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'


class IsTraderOrCustomerReadOnly(BasePermission):
    """Allows traders and customers to only view products."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["trader", "customer"]

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return False


class IsOwner(BasePermission):
    """Allows access only to the owner of the object."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Ensuring users can only access their own orders/transactions