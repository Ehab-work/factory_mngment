from rest_framework.permissions import BasePermission

class IsSalesRep(BasePermission):
    """
    Permission to allow only Sales Representatives to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_rep'
    
    def has_object_permission(self, request, view, obj):
        # Sales Rep can only access their own resources
        if hasattr(obj, 'employee') and hasattr(obj.employee, 'user'):
            return obj.employee.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsSalesSupervisor(BasePermission):
    """
    Permission to allow only Sales Supervisors to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales_supervisor'
    
    def has_object_permission(self, request, view, obj):
        # Sales Supervisor can access their team's resources or their own
        if hasattr(obj, 'employee') and hasattr(obj.employee, 'department'):
            # Example for department or team-based access
            return True  # Implement actual team logic
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsPurchasingOfficer(BasePermission):
    """
    Permission to allow only Purchasing Officers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'purchasing_officer'
    
    def has_object_permission(self, request, view, obj):
        # Purchasing Officer can access purchasing resources or their own
        if hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsWorker(BasePermission):
    """
    Permission to allow only Workers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'worker'
    
    def has_object_permission(self, request, view, obj):
        # Worker can only access their own resources
        if hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsProductionSupervisor(BasePermission):
    """
    Permission to allow only Production Supervisors to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'production_supervisor'
    
    def has_object_permission(self, request, view, obj):
        # Production Supervisor can access their team's resources or their own
        if hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsStoreKeeper(BasePermission):
    """
    Permission to allow only Store Keepers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'store_keeper'
    
    def has_object_permission(self, request, view, obj):
        # Store Keeper can access inventory resources or their own user data
        if hasattr(obj, 'id'):
            return obj.id == request.user.id
        return False

class IsAdmin(BasePermission):
    """
    Permission to allow only Admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        # Admin has full access
        return True

class IsOwnerOrAdmin(BasePermission):
    """
    Permission to allow only the owner of an object or an admin to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow if admin
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
            
        # Check if obj has user attribute or is a user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'id'):  
            return obj.id == request.user.id
            
        return False