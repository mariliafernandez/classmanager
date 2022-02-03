from rest_framework.permissions import IsAuthenticated, AllowAny

class ActionBasedPermission(AllowAny):
    def has_permission(self, request, view):
        for _class, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return _class().has_permission(request, view)
        return False
