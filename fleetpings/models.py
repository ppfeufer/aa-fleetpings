"""
Our models
"""

# Standard Library
import re

# Third Party
from requests.exceptions import HTTPError

# Django
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# AA Fleet Pings
from fleetpings.app_settings import (
    AA_FLEETPINGS_WEBHOOK_VERIFICATION,
    discord_service_installed,
)

# Check if the Discord service is active
from fleetpings.constants import DISCORD_WEBHOOK_REGEX

if discord_service_installed():
    # Alliance Auth
    from allianceauth.services.modules.discord.models import DiscordUser


def _get_discord_group_info(ping_target: Group) -> dict:
    """
    Get Discord group info or raise an error
    :param ping_target:
    :type ping_target:
    :return:
    :rtype:
    """

    if not discord_service_installed():
        raise ValidationError(
            _("You might want to install the Discord service first ...")
        )

    try:
        discord_group_info = DiscordUser.objects.group_to_role(group=ping_target)
    except HTTPError as http_error:
        raise ValidationError(
            _("Are you sure you have your Discord linked to your Alliance Auth?")
        ) from http_error
    else:
        if not discord_group_info:
            raise ValidationError(_("This group has not been synced to Discord yet."))

        return discord_group_info


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

    # Doctrine name
    name = models.CharField(
        max_length=255, unique=True, help_text=_("Short name to identify this doctrine")
    )

    # Link to your doctrine
    link = models.CharField(
        max_length=255,
        help_text=_("A link to a doctrine page for this doctrine if you have."),
        blank=True,
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleetdoctrine_require_groups",
        help_text=_("Restrict this doctrine to the following group(s) ..."),
    )

    # Doctrine notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # Is doctrine active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this doctrine is enabled or not"),
    )

    def clean(self):
        """
        Check if the doctrine link is an actual link to a website
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

    # Formup location notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # Is formup location active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

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

    # Discord group to ping
    name = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        unique=True,
        help_text=(
            _(
                "Name of the Discord role to ping. "
                "(Note: This must be an Auth group that is synced to Discord.)"
            )
        ),
    )

    # Discord group id
    discord_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("ID of the Discord role to ping"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="discord_role_require_groups",
        help_text=_("Restrict ping rights to the following group(s) ..."),
    )

    # Notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # Is this group active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
    )

    def clean(self):
        """
        Check if the group has already been synced to Discord,
        if not, raise an error
        """

        _get_discord_group_info(self.name)

        super().clean()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Add the Discord group ID (if Discord service is active) and save the whole thing
        """

        # Check if the Discord service is active
        if discord_service_installed():
            discord_group_info = _get_discord_group_info(self.name)
            self.discord_id = discord_group_info["id"]

        super().save()  # Call the "real" save() method.

    def __str__(self) -> str:
        return str(self.name)

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

    # Name of the fleet type
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Short name to identify this fleet type"),
    )

    # Embed color
    embed_color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_("Hightlight color for the embed"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleettype_require_groups",
        help_text=_("Restrict this fleet type to the following group(s) ..."),
    )

    # Fleet type notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
    )

    # Is this fleet type enabled
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this fleet type is enabled or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

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
    A Discord webhook
    """

    # Channel name
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Name of the channel this webhook posts to"),
    )

    # Wehbook url
    url = models.CharField(
        max_length=255,
        unique=True,
        help_text=(
            _(
                "URL of this webhook, e.g. "
                "https://discord.com/api/webhooks/123456/abcdef"
            )
        ),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="webhook_require_groups",
        help_text=_("Restrict ping rights to the following group(s) ..."),
    )

    # Webhook notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this webhook here if you want"),
    )

    # Is it enabled
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this webhook is active or not"),
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Webhook :: Meta
        """

        verbose_name = _("Webhook")
        verbose_name_plural = _("Webhooks")
        default_permissions = ()

    def clean(self):
        """
        Check if the webhook URL is valid
        :return:
        """

        # Check if it's an actual webhook url if the verification setting is set.
        if (
            not re.match(DISCORD_WEBHOOK_REGEX, self.url)
            and AA_FLEETPINGS_WEBHOOK_VERIFICATION
        ):
            raise ValidationError(
                _(
                    "Invalid webhook URL. The webhook URL you entered does not match "
                    "any known format for a Discord webhook. Please check the "
                    "webhook URL."
                )
            )

        super().clean()
