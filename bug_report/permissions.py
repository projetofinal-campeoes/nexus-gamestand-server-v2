from rest_framework import permissions
from rest_framework.views import Request

class WriteOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method == 'POST':
            return True
        
        return (request.user.is_superuser and request.user.is_authenticated)