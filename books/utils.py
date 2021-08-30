from django.core.exceptions import PermissionDenied


class IsOwnerOrStaff:
    """
    Return object if user is owner or is_staff.
    """
    def get_object(self, queryset=None):
        obj = super(IsOwnerOrStaff, self).get_object(queryset)
        if self.request.user == obj.user or self.request.user.is_staff:
            return obj
        raise PermissionDenied('You don\'t have a permissions to do this.')
