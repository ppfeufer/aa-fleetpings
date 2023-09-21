# Django
from django.db import migrations

# Alliance Auth (External Libs)
from app_utils.app_settings import clean_setting

use_doctrines_from_fittings_module = clean_setting(
    "AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE", False
)

webhook_verification = clean_setting("AA_FLEETPINGS_WEBHOOK_VERIFICATION", True)


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
        pk=1,
        use_doctrines_from_fittings_module=use_doctrines_from_fittings_module,
        webhook_verification=webhook_verification,
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
