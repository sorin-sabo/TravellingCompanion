# Django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local App
from apps.core.managers import AuthManager, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom authentication User model with admin-compliant permissions.
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # DATABASE FIELDS
    id = models.AutoField(primary_key=True, db_column='user_id')
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
        validators=[validate_email]
    )
    status = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_('Designates whether the user is active or not.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    # AUDIT FIELDS
    last_login_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    # MANAGERS
    objects = AuthManager()
    entities = UserManager()

    # META CLASS
    class Meta:
        db_table = 'user'
        app_label = 'core'
        verbose_name = 'User'

    # TO STRING METHOD
    def __str__(self):
        return str(self.email)
