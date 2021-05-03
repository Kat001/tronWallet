from rest_framework.permissions import BasePermission

class IsCourseInstructor(BasePermission):

    def has_permission(self, request, view):
        is_allowed_user = False
        try:
            if request.user.role == 'SCHOOL':
                is_allowed_user = True
        except Exception as e:
            is_allowed_user = False
        return is_allowed_user

