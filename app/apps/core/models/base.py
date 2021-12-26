# Django
from django.db import models

# Local App
from .user import User


class BaseModel(models.Model):
    """
    Audit fields to be extended in all models.
    """

    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        db_column='created_by',
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        db_column='updated_by',
        related_name="%(class)s_updated_by",
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        auto_now=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "General Configuration"
