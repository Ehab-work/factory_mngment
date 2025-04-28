from rest_framework.permissions import BasePermission

class IsSalesRep(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_rep'

class IsSalesSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_supervisor'

class IsPurchasingOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'purchasing_officer'

class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'worker'

class IsProductionSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'production_supervisor'

class IsStoreKeeper(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'store_keeper'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'