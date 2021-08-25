from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin


class IsAuthorOrStaffMixin:
    """
    Return object if user is author owner or is_staff.
    """
    def get_object(self, queryset=None):
        obj = super(IsAuthorOrStaffMixin, self).get_object(queryset)
        if self.request.user in obj.authors.all() or self.request.user.is_staff:
            return obj
        raise PermissionDenied


class IsOwnerOrStaff:
    """
    Return object if user is owner or is_staff.
    """
    def get_object(self, queryset=None):
        obj = super(IsOwnerOrStaff, self).get_object(queryset)
        if self.request.user == obj.user or self.request.user.is_staff:
            return obj
        raise PermissionDenied
