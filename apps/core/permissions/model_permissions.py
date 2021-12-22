# Standard library
import copy

# Rest Framework
from rest_framework import permissions


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    """
    Generic permission for getters
    """
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
