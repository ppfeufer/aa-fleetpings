# -*- coding: utf-8 -*-

"""
settings for the admin backend
"""

from fleetpings.form import FleetTypeAdminForm
from fleetpings.models import (
    FleetComm,
    Webhook,
    FleetDoctrine,
    FormupLocation,
    DiscordPingTargets,
    FleetType,
)

from django.contrib import admin


def custom_filter_title(title):
    class Wrapper(admin.FieldListFilter):
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

    def _name(self, obj):
        return obj.name

    _name.short_description = "Fleet Comms"
    _name.admin_order_field = "name"


@admin.register(FleetDoctrine)
class FleetDoctrineAdmin(admin.ModelAdmin):
    """
    FleetDoctrineAdmin
    """

    list_display = ("_name", "_link", "_restricted_to_group", "notes", "is_enabled")
    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter_title("active")),
        ("restricted_to_group", custom_filter_title("restriction")),
    )

    def _name(self, obj):
        return obj.name

    _name.short_description = "Doctrine"
    _name.admin_order_field = "name"

    def _link(self, obj):
        return obj.name

    _link.short_description = "Doctrine Link"
    _link.admin_order_field = "link"

    def _restricted_to_group(self, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)
        else:
            return None

    _restricted_to_group.short_description = "Restricted to"
    _restricted_to_group.admin_order_field = "restricted_to_group__name"


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
        ("is_enabled", custom_filter_title("active")),
        ("name", custom_filter_title("target")),
        ("restricted_to_group", custom_filter_title("restriction")),
    )

    def _name(self, obj):
        return obj.name

    _name.short_description = "Ping Target"
    _name.admin_order_field = "name"

    def _restricted_to_group(self, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)
        else:
            return None

    _restricted_to_group.short_description = "Restricted to"
    _restricted_to_group.admin_order_field = "restricted_to_group__name"


@admin.register(FleetType)
class FleetTypeAdmin(admin.ModelAdmin):
    """
    FleetTypeAdmin
    """

    form = FleetTypeAdminForm

    list_display = (
        "_name",
        "embed_color",
        "_restricted_to_group",
        "notes",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter_title("active")),
        ("restricted_to_group", custom_filter_title("restriction")),
    )

    def _name(self, obj):
        return obj.name

    _name.short_description = "Fleet Type"
    _name.admin_order_field = "name"

    def _restricted_to_group(self, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)
        else:
            return None

    _restricted_to_group.short_description = "Restricted to"
    _restricted_to_group.admin_order_field = "restricted_to_group__name"


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """
    WebhookAdmin
    """

    list_display = (
        # "id",
        "_name",
        "_type",
        "_url",
        "_restricted_to_group",
        "notes",
        "is_embedded",
        "is_enabled",
    )

    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)

    list_filter = (
        ("is_enabled", custom_filter_title("active")),
        ("is_embedded", custom_filter_title("embedded")),
        ("type", custom_filter_title("webhook type")),
        ("restricted_to_group", custom_filter_title("restriction")),
    )

    def _name(self, obj):
        return obj.name

    _name.short_description = "Channel Name"
    _name.admin_order_field = "name"

    def _type(self, obj):
        return obj.type

    _type.short_description = "Webhook Type"
    _type.admin_order_field = "type"

    def _url(self, obj):
        return obj.url

    _url.short_description = "Webhook URL"
    _url.admin_order_field = "url"

    def _restricted_to_group(self, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)
        else:
            return None

    _restricted_to_group.short_description = "Restricted to"
    _restricted_to_group.admin_order_field = "restricted_to_group__name"
