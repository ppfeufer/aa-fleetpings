# Django
from django.db import migrations

default_settings_to_migrate = [
    {"variable": "useDefaultFleetTypes", "value": True},
    {"variable": "usedefaultPingTargets", "value": True},
]


def on_migrate(apps, schema_editor):
    """
    Create default settings on migration
    :param apps:
    :param schema_editor:
    :return:
    """

    Setting = apps.get_model("fleetpings", "Setting")
    db_alias = schema_editor.connection.alias

    Setting.objects.using(db_alias).create(pk=1)


def on_migrate_zero(apps, schema_editor):
    """
    Remove default settings on migratio to zero
    :param apps:
    :param schema_editor:
    :return:
    """

    Setting = apps.get_model("fleetpings", "Setting")
    db_alias = schema_editor.connection.alias
    Setting.objects.using(db_alias).delete()


class Migration(migrations.Migration):
    """
    Run migrations
    """

    dependencies = [
        ("fleetpings", "0011_setting"),
    ]

    operations = [migrations.RunPython(on_migrate, on_migrate_zero)]
