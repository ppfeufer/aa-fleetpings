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


@admin.register(FleetComm)
class FleetCommAdmin(admin.ModelAdmin):
    """
    FleetCommAdmin
    """

    list_display = ("name", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(FleetDoctrine)
class FleetDoctrineAdmin(admin.ModelAdmin):
    """
    FleetDoctrineAdmin
    """

    list_display = ("name", "link", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)


@admin.register(FormupLocation)
class FormupLocationAdmin(admin.ModelAdmin):
    """
    FormupLocationAdmin
    """

    list_display = ("name", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(DiscordPingTargets)
class DiscordPingTargetsAdmin(admin.ModelAdmin):
    """
    DiscordPingTargetsAdmin
    """

    list_display = ("name", "discord_id", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)
    filter_horizontal = ("restricted_to_group",)
    readonly_fields = ("discord_id",)


@admin.register(FleetType)
class FleetTypeAdmin(admin.ModelAdmin):
    """
    FleetTypeAdmin
    """

    form = FleetTypeAdminForm
    list_display = ("name", "embed_color", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    filter_horizontal = ("restricted_to_group",)
    ordering = ("name",)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """
    WebhookAdmin
    """

    list_display = (
        # "id",
        "name",
        "type",
        "url",
        "notes",
        "is_embedded",
        "is_enabled",
    )
    list_filter = ("is_enabled",)
    ordering = ("name",)
    filter_horizontal = ("restricted_to_group",)
