from rest_framework import permissions

class IsPurchasingOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'purchasing_officer'

class IsStoreKeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'store_keeper'