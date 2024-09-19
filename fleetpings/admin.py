"""
AA Fleet Pings :: Admin
"""

# Third Party
from solo.admin import SingletonModelAdmin

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# AA Fleet Pings
from fleetpings.form import FleetTypeAdminForm, SettingAdminForm
from fleetpings.models import (
    DiscordPingTarget,
    FleetComm,
    FleetDoctrine,
    FleetType,
    FormupLocation,
    Setting,
    Webhook,
)


def custom_filter(title) -> admin.FieldListFilter:
    """
    Custom filter for model properties

    :param title:
    :type title:
    :return:
    :rtype:
    """

    class Wrapper(admin.FieldListFilter):
        """
        Wrapper
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

    list_display = ("_name", "channel", "notes", "is_enabled")
    ordering = ("name", "channel")
    list_filter = ("is_enabled",)

    @classmethod
    @admin.display(description=_("Fleet comm"), ordering="name")
    def _name(cls, obj: FleetComm) -> str:
        """
        _name

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

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
    @admin.display(description=_("Doctrine"), ordering="name")
    def _name(cls, obj: FleetDoctrine) -> str:
        """
        _name

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @classmethod
    @admin.display(description=_("Doctrine link"), ordering="link")
    def _link(cls, obj: FleetDoctrine) -> str:
        """
        _link

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @classmethod
    @admin.display(
        description=_("Group restrictions"), ordering="restricted_to_group__name"
    )
    def _restricted_to_group(cls, obj: FleetDoctrine) -> str | None:
        """
        _restricted_to_group

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

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


@admin.register(DiscordPingTarget)
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
    @admin.display(description=_("Ping target"), ordering="name")
    def _name(cls, obj: DiscordPingTarget) -> Group:
        """
        _name

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @classmethod
    @admin.display(
        description=_("Group restrictions"), ordering="restricted_to_group__name"
    )
    def _restricted_to_group(cls, obj: DiscordPingTarget) -> str | None:
        """
        _restricted_to_group

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

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
    @admin.display(description=_("Fleet type"), ordering="name")
    def _name(cls, obj: FleetType) -> str:
        """
        _name

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @classmethod
    @admin.display(description=_("Embed color"), ordering="embed_color")
    def _embed_color(cls, obj: FleetType) -> str:
        """
        _embed_color

        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return_value = (
            "<span "
            'style="display: inline-block; width: 16px; background-color: {bg_color};">'
            "&nbsp;&nbsp;"
            "</span> {bg_color}".format(bg_color=obj.embed_color)
        )

        return mark_safe(return_value)

    @classmethod
    @admin.display(
        description=_("Group restrictions"), ordering="restricted_to_group__name"
    )
    def _restricted_to_group(cls, obj: FleetType) -> str | None:
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
    @admin.display(description=_("Discord channel"), ordering="name")
    def _name(cls, obj: Webhook) -> str:
        return obj.name

    @classmethod
    @admin.display(description=_("Webhook URL"), ordering="url")
    def _url(cls, obj: Webhook) -> str:
        return obj.url

    @classmethod
    @admin.display(
        description=_("Group restrictions"), ordering="restricted_to_group__name"
    )
    def _restricted_to_group(cls, obj: Webhook) -> str | None:
        names = [x.name for x in obj.restricted_to_group.all().order_by("name")]

        if names:
            return ", ".join(names)

        return None


@admin.register(Setting)
class SettingAdmin(SingletonModelAdmin):
    """
    Setting Admin
    """

    form = SettingAdminForm
