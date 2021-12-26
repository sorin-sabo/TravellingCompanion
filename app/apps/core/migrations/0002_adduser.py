from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


# noinspection PyUnusedLocal,PyPep8Naming,SpellCheckingInspection
def manage_permissions(apps, schema_editor):
    """
    Manage permissions

    - Add permission groups
    - Assign permissions to groups
    """

    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, 'default')

    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')

    # Add groups
    initial_auth_groups = [
        dict(id=1, name='passenger'),
        dict(id=2, name='guest'),
    ]

    for group_dict in initial_auth_groups:
        group = Group(**group_dict)
        group.save()

    # Assign permissions to groups
    passenger_permission_codes = [
        'view_destination',
        'add_destination',
        'change_destination',
        'add_passenger',
        'delete_passenger',
        'view_passenger',
        'add_trip',
        'change_trip',
        'view_trip',
        'delete_trip',
        'change_tripdestination',
        'view_tripdestination'
    ]
    passenger_permissions = []

    for code in passenger_permission_codes:
        permission = (
            Permission
            .objects
            .filter(codename=code)
            .values('id')
            .order_by('-id')
            .first()
        )

        if permission is not None:
            passenger_permissions.append(permission.get('id'))

    passenger_group = Group.objects.get_by_natural_key('passenger')
    passenger_group.permissions.set(passenger_permissions)
    passenger_group.save()

    guest_permission_codes = [
        'view_destination',
        'view_trip',
    ]
    guest_permissions = []

    for code in guest_permission_codes:
        permission = (
            Permission
            .objects
            .filter(codename=code)
            .values('id')
            .order_by('-id')
            .first()
        )

        if permission is not None:
            guest_permissions.append(permission.get('id'))

    guest_group = Group.objects.get_by_natural_key('guest')
    guest_group.permissions.set(guest_permissions)
    guest_group.save()


# noinspection PyUnusedLocal,PyPep8Naming
def add_demo_user(apps, schema_editor):
    """
    Manage permissions

    - Add permission groups
    - Assign permissions to groups
    """

    User = apps.get_model('core', 'User')
    Group = apps.get_model('auth', 'Group')

    user_dict = {
        "id": 1,
        "email": "demo@travel.com",
        "is_staff": False,
        "status": True
    }

    existing_user = User.objects.filter(id=user_dict['id']).first()
    passenger_group = Group.objects.get_by_natural_key('passenger')

    if not existing_user:
        user = User(**user_dict)
        user.save()
        user.groups.set([passenger_group.pk])
    else:
        existing_user.groups.set([passenger_group.pk])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('sites', '0002_alter_domain_unique')
    ]

    operations = [
        migrations.RunPython(manage_permissions),
        migrations.RunPython(add_demo_user)
    ]
