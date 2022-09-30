from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    # permission_classes = [UserNameContainsCFEPermission, IsStaffEditorPermission]

