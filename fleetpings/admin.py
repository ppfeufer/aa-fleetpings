"""
Settings for the admin backend
"""

# Django
from django.contrib import admin
from django.utils.safestring import mark_safe

# AA Fleet Pings
from fleetpings.form import FleetTypeAdminForm
from fleetpings.models import (
    DiscordPingTargets,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Webhook,
)


def custom_filter(title):
    """
    Custom filter for model properties
    :param title:
    :return:
    """

    class Wrapper(admin.FieldListFilter):
        """
        Custom_filter :: Wrapper
        """

        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


@admin.register(FleetComm)
class FleetCommAdmin(admin.ModelAdmin):
    """
    FleetCommAdmin
    """

    list_display = ("_name", "notes", "is_enabled")
    ordering = ("name",)
    list_filter = ("is_enabled",)

    @classmethod
    @admin.display(description="Fleet Comms", ordering="name")
    def _name(cls, obj):
        return obj.name


@admin.register(FleetDoctrine)
class FleetDoctrineAdmin(admin.ModelAdmin):
    """
    FleetDoctrineAdmin
    """

    list_display = ("_name", "_link", "_restricted_to_group", "notes", "is_enabled")
    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter(title="active")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    @admin.display(description="Doctrine", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Doctrine Link", ordering="link")
    def _link(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None


@admin.register(FormupLocation)
class FormupLocationAdmin(admin.ModelAdmin):
    """
    FormupLocationAdmin
    """

    list_display = ("name", "notes", "is_enabled")
    ordering = ("name",)
    list_filter = ("is_enabled",)


@admin.register(DiscordPingTargets)
class DiscordPingTargetsAdmin(admin.ModelAdmin):
    """
    DiscordPingTargetsAdmin
    """

    list_display = (
        "_name",
        "discord_id",
        "_restricted_to_group",
        "notes",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    readonly_fields = ("discord_id",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter(title="active")),
        ("name", custom_filter(title="target")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    @admin.display(description="Ping Target", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None


@admin.register(FleetType)
class FleetTypeAdmin(admin.ModelAdmin):
    """
    FleetTypeAdmin
    """

    form = FleetTypeAdminForm

    list_display = (
        "_name",
        "_embed_color",
        "_restricted_to_group",
        "notes",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter(title="active")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    @admin.display(description="Fleet Type", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Embed Color", ordering="embed_color")
    def _embed_color(cls, obj):
        return_value = (
            "<span "
            'style="display: inline-block; width: 16px; background-color: {bg_color};">'
            "&nbsp;&nbsp;"
            "</span> {bg_color}".format(bg_color=obj.embed_color)
        )

        return mark_safe(return_value)

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """
    WebhookAdmin
    """

    list_display = (
        "_name",
        "_url",
        "_restricted_to_group",
        "notes",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter(title="active")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    @admin.display(description="Channel Name", ordering="name")
    def _name(cls, obj):
        return obj.name

    @classmethod
    @admin.display(description="Webhook URL", ordering="url")
    def _url(cls, obj):
        return obj.url

    @classmethod
    @admin.display(description="Restricted to", ordering="restricted_to_group__name")
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None
