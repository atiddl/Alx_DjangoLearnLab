from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post/comment to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS => allow read-only access
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
