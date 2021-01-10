# -*- coding: utf-8 -*-

"""
settings for the admin backend
"""
from django.utils.safestring import mark_safe
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


def custom_filter(title):
    """
    custom filter for model properties
    :param title:
    :return:
    """

    class Wrapper(admin.FieldListFilter):
        """
        custom_filter :: wrapper
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
    def _name(cls, obj):
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
        ("is_enabled", custom_filter(title="active")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    def _name(cls, obj):
        return obj.name

    _name.short_description = "Doctrine"
    _name.admin_order_field = "name"

    @classmethod
    def _link(cls, obj):
        return obj.name

    _link.short_description = "Doctrine Link"
    _link.admin_order_field = "link"

    @classmethod
    def _restricted_to_group(cls, obj):
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
        ("is_enabled", custom_filter(title="active")),
        ("name", custom_filter(title="target")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    def _name(cls, obj):
        return obj.name

    _name.short_description = "Ping Target"
    _name.admin_order_field = "name"

    @classmethod
    def _restricted_to_group(cls, obj):
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
    def _name(cls, obj):
        return obj.name

    _name.short_description = "Fleet Type"
    _name.admin_order_field = "name"

    @classmethod
    def _embed_color(cls, obj):
        return_value = (
            "<span "
            'style="display: inline-block; width: 16px; background-color: {bg_color};">'
            "&nbsp;&nbsp;"
            "</span> {bg_color}".format(bg_color=obj.embed_color)
        )

        return mark_safe(return_value)

    _embed_color.short_description = "Embed Color"
    _embed_color.admin_order_field = "embed_color"

    @classmethod
    def _restricted_to_group(cls, obj):
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
        ("is_enabled", custom_filter(title="active")),
        ("is_embedded", custom_filter(title="embedded")),
        ("type", custom_filter(title="webhook type")),
        ("restricted_to_group", custom_filter(title="restriction")),
    )

    @classmethod
    def _name(cls, obj):
        return obj.name

    _name.short_description = "Channel Name"
    _name.admin_order_field = "name"

    @classmethod
    def _type(cls, obj):
        return obj.type

    _type.short_description = "Webhook Type"
    _type.admin_order_field = "type"

    @classmethod
    def _url(cls, obj):
        return obj.url

    _url.short_description = "Webhook URL"
    _url.admin_order_field = "url"

    @classmethod
    def _restricted_to_group(cls, obj):
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)
        else:
            return None

    _restricted_to_group.short_description = "Restricted to"
    _restricted_to_group.admin_order_field = "restricted_to_group__name"
