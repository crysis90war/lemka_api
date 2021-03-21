from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UserGetPostPermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    my_safe_method = ['GET', 'POST']

    # my_safe_method = ['GET', 'PUT']
    # my_safe_method = ['GET']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UserRUDPermission(permissions.BasePermission):
    my_safe_method = ['GET', 'PUT', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in self.my_safe_method:
            return True
        return obj.id == request.user.id


class OnlyOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.ref_user == request.user


# class IsAuthenticatedOwner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # work when your access /item/
#         if request.user and is_authenticated(request.user):
#             if request.user.id in [1, 2, 3]:
#                 return True
#             else:
#                 return False
#         else:
#             return False
#
#     def has_object_permission(self, request, view, obj):
#         # work when your access /item/item_id/
#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.ref_user_mensuration.ref_user == request.user or request.user.is_admin
