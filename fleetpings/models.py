# -*- coding: utf-8 -*-

"""
our models
"""

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from requests.exceptions import HTTPError

from fleetpings.app_settings import discord_service_installed

from allianceauth.services.modules.discord.models import DiscordUser


class AaFleetpings(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        AaFleetpings :: Meta
        """

        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)


# FleetComm Model
class FleetComm(models.Model):
    """
    Fleet Comms
    """

    name = models.CharField(
        max_length=255, unique=True, help_text=_("Short name to identify this comms")
    )

    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this comms is enabled or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FleetComm :: Meta
        """

        verbose_name = _("Fleet Comm")
        verbose_name_plural = _("Fleet Comms")
        default_permissions = ()


# FleetDoctrine Model
class FleetDoctrine(models.Model):
    """
    Fleet Doctrine
    """

    # doctrine name
    name = models.CharField(
        max_length=255, unique=True, help_text=_("Short name to identify this doctrine")
    )

    # link to your doctinre
    link = models.CharField(
        max_length=255,
        help_text=_("A link to a doctrine page for this doctrine if you have."),
        blank=True,
    )

    # restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleetdoctrine_require_groups",
        help_text=_("Restrict this doctrine to the following group(s) ..."),
    )

    # doctrine notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # is doctrine active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this doctrine is enabled or not"),
    )

    def clean(self):
        """
        check if the doctrine link is an actual link to a website
        """

        doctrine_link = self.link

        if doctrine_link != "":
            validate = URLValidator()

            try:
                validate(doctrine_link)
            except ValidationError as exception:
                raise ValidationError(
                    _("Your doctrine URL is not valid.")
                ) from exception

        super().clean()

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FleetDoctrine :: Meta
        """

        verbose_name = _("Fleet Doctrine")
        verbose_name_plural = _("Fleet Doctrines")
        default_permissions = ()


# FormupLocation Model
class FormupLocation(models.Model):
    """
    Formup Location
    """

    # formup location name
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Short name to identify this formup location"),
    )

    # formup location notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # is formup location active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FormupLocation :: Meta
        """

        verbose_name = _("Formup Location")
        verbose_name_plural = _("Formup Locations")
        default_permissions = ()


# DiscordPingTargets Model
class DiscordPingTargets(models.Model):
    """
    Discord Ping Targets
    """

    # discord group to ping
    name = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        unique=True,
        help_text=(
            _(
                "Name of the Discord role to ping. "
                "(Note: This must be an Auth group that is synched to Discord.)"
            )
        ),
    )

    # discord group id
    discord_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("ID of the Discord role to ping"),
    )

    # restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="discord_role_require_groups",
        help_text=_("Restrict ping rights to the following group(s) ..."),
    )

    # notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # is this group active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
    )

    def clean(self):
        """
        check if the group has already been synched to Discord,
        if not, raise an error
        """

        # check if the Discord service is active
        if not discord_service_installed():
            raise ValidationError(
                _("You might want to install the Discord service first ...")
            )

        # get the group id from Discord
        try:
            discord_group_info = DiscordUser.objects.group_to_role(self.name)
        except HTTPError:
            raise ValidationError(
                _("Are you sure you have your Discord linked to your Alliance Auth?")
            )
        else:
            if not discord_group_info:
                raise ValidationError(
                    _("This group has not been synched to Discord yet.")
                )

        super().clean()

    def save(self):
        """
        Add the Discord group ID and save the whole thing
        """

        discord_group_info = DiscordUser.objects.group_to_role(self.name)
        self.discord_id = discord_group_info["id"]
        super().save()  # Call the "real" save() method.

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"discord_id='{self.discord_id}', "
            f"restricted_to_group='{self.restricted_to_group.all()}', "
            f"name='{self.name}'"
            f") "
        )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        DiscordPingTargets :: Meta
        """

        verbose_name = _("Discord Ping Target")
        verbose_name_plural = _("Discord Ping Targets")
        default_permissions = ()


# FleetType Model
class FleetType(models.Model):
    """
    Fleet Types
    """

    # name of the fleet type
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Short name to identify this fleet type"),
    )

    # embed color
    embed_color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_("Hightlight color for the embed"),
    )

    # restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleettype_require_groups",
        help_text=_("Restrict this fleet type to the following group(s) ..."),
    )

    # fleet type notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # is this fleet type enabled
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this fleet type is enabled or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}')"

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FleetType :: Meta
        """

        verbose_name = _("Fleet Type")
        verbose_name_plural = _("Fleet Types")
        default_permissions = ()


# Webhook Model
class Webhook(models.Model):
    """
    A Discord or Slack webhook
    """

    # webhook type choices
    WEBHOOK_TYPE_DISCORD = "Discord"
    WEBHOOK_TYPE_SLACK = "Slack"
    WEBHOOK_TYPE_CHOICES = (
        (WEBHOOK_TYPE_DISCORD, "Discord"),
        (WEBHOOK_TYPE_SLACK, "Slack"),
    )

    # webhook type
    type = models.CharField(
        max_length=7,
        choices=WEBHOOK_TYPE_CHOICES,
        default=WEBHOOK_TYPE_DISCORD,
        help_text=_("Is this a Discord or Slack webhook?"),
    )

    # channel name
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Name of the channel this webhook posts to"),
    )

    # wehbook url
    url = models.CharField(
        max_length=255,
        unique=True,
        help_text=(
            _(
                "URL of this webhook, e.g. "
                "https://discordapp.com/api/webhooks/123456/abcdef "
                "or https://hooks.slack.com/services/xxxx/xxxx"
            )
        ),
    )

    # embedded ping (only for discord wenhooks)
    is_embedded = models.BooleanField(
        default=True,
        db_index=True,
        help_text=(
            _(
                "Whether this webhook's ping is embedded or not. "
                "(This setting only effects Discord webhooks.)"
            )
        ),
    )

    # restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="webhook_require_groups",
        help_text=_("Restrict ping rights to the following group(s) ..."),
    )

    # webhook notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this webhook here if you want"),
    )

    # is it enabled
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this webhook is active or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"type='{self.type}', "
            f"url='{self.url}', "
            f"restricted_to_group='{self.restricted_to_group.all()}', "
            f"name='{self.name}', "
            f"is_embedded='{self.is_embedded}'"
            f")"
        )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Webhook :: Meta
        """

        verbose_name = _("Webhook")
        verbose_name_plural = _("Webhooks")
        default_permissions = ()
