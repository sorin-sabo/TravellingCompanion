# Rest Framework
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class CanSeeApiDocs(BasePermission):
    """
    Allow only admin user to see api docs
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_staff and request.user.is_superuser
