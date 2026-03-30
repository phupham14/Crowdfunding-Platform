from rest_framework.permissions import BasePermission, SAFE_METHODS

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        # Public actions
        if view.action in ['list', 'retrieve']:
            return True

        # Các action cần login
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin → full quyền
        if user.is_authenticated and user.role == "ADMIN":
            return True

        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            # Owner xem mọi trạng thái
            if user.is_authenticated and obj.owner == user:
                return True

            # Public chỉ xem OPEN
            return obj.status == "OPEN"

        # Write actions → chỉ owner
        return obj.owner == user