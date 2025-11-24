# Django
from django.db import migrations


def on_migrate(apps, schema_editor):
    """
    Create default settings on migration
    :param apps:
    :param schema_editor:
    :return:
    """

    Setting = apps.get_model("fleetpings", "Setting")
    db_alias = schema_editor.connection.alias

    Setting.objects.using(db_alias).create(
        pk=1, use_doctrines_from_fittings_module=False, webhook_verification=True
    )


def on_migrate_zero(apps, schema_editor):
    """
    Remove default settings on migration to zero
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
        ("fleetpings", "0011_settings_and_verbose_names"),
    ]

    operations = [migrations.RunPython(on_migrate, on_migrate_zero)]
