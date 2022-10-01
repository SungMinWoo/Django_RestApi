from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    # permission_classes = [UserNameContainsCFEPermission, IsStaffEditorPermission]


class UserQuerysetMixin():
    user_field = 'user'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if user.is_staff: # 스텝이면 쿼리셋 전체 반환
            return qs
        return qs.filter(**lookup_data)
