# Django
from django.contrib.auth.models import BaseUserManager
from django.db import models

# Rest Framework
from rest_framework.exceptions import PermissionDenied


class AuthManager(BaseUserManager):
    """
    Authentication Manager
    """
    def get_or_create_for_oauth2(self, payload):
        """
        Get internal user by authentication email

        Function triggered after token validation was successfully accomplished
        Customise this function based on the BL approved.
        - if a user is not found in the system an error is raised; this can be changed to a user
        is created;
        - if a user status is inactive an error is raised;
        - last login datetime is updated;

        :param payload: External auth service received payload
        :return:
        """

        if 'email' in payload:
            email = payload['email']

            try:
                user = self.get(email=email)

            except self.model.DoesNotExist:
                raise PermissionDenied('Logged in user does not exist in the system. '
                                       'Please contact system administrator for more information.')

            if not user.status:
                raise PermissionDenied('Logged in user is inactive. '
                                       'Please contact system administrator for more information.')

            user.save(update_fields=['last_login_at'])  # update login date

        else:  # GUEST USER
            user = self.get(email='guest@guest.com')

        return user

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserManager(models.Manager):
    def get(self, user_id=None, email=None):
        """
        Get user by pk or email

        :param int user_id: User id to check if corresponding user exists; if provided
        email param is redundant
        :param str email: User email to check if corresponding user exists
        :return: User found with provided id/email or None in case user not found
        """

        if user_id is None and email is None:
            return None

        # Check user exists by id
        if user_id is not None:
            filters = dict(id=user_id)
        else:
            filters = dict(email=email)

        return (
            super()
            .get_queryset()
            .filter(**filters)
            .first()
        )
