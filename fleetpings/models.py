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
from fleetpings.app_settings import discord_service_installed
from fleetpings.constants import DISCORD_WEBHOOK_REGEX
from fleetpings.managers import SettingManager

# Check if the Discord service is active
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
            _("You might want to install the Discord service first …")
        )

    try:
        discord_group_info = DiscordUser.objects.group_to_role(group=ping_target)
    except HTTPError as http_error:
        raise ValidationError(
            _("Are you sure you have your Discord linked to your Alliance Auth?")
        ) from http_error

    if not discord_group_info:
        raise ValidationError(_("This group has not been synced to Discord yet."))

    return discord_group_info


class SingletonModel(models.Model):
    """
    SingletonModel
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Model meta definitions
        """

        abstract = True

    def save(self, *args, **kwargs):
        """
        Save action
        :param args:
        :param kwargs:
        :return:
        """

        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete action
        :param args:
        :param kwargs:
        :return:
        """

        pass  # pylint: disable=unnecessary-pass


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
        max_length=255,
        help_text=_("Short name to identify this comms"),
        verbose_name=_("Name"),
    )

    channel = models.CharField(
        blank=True,
        max_length=255,
        help_text=_("In which channel is the fleet?"),
        verbose_name=_("Channel"),
    )

    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
        verbose_name=_("Notes"),
    )

    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this comms is enabled or not"),
        verbose_name=_("Is enabled"),
    )

    def __str__(self) -> str:
        return f"{self.name} » {self.channel}" if self.channel else f"{self.name}"

    class Meta:  # pylint: disable=too-few-public-methods
        """
        FleetComm :: Meta
        """

        verbose_name = _("Fleet Comm")
        verbose_name_plural = _("Fleet Comms")
        default_permissions = ()

        unique_together = ("name", "channel")


# FleetDoctrine Model
class FleetDoctrine(models.Model):
    """
    Fleet Doctrine
    """

    # Doctrine name
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Short name to identify this doctrine"),
        verbose_name=_("Name"),
    )

    # Link to your doctrine
    link = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("A link to a doctrine page for this doctrine if you have."),
        verbose_name=_("Doctrine link"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleetdoctrine_require_groups",
        help_text=_("Restrict this doctrine to the following groups …"),
        verbose_name=_("Group restrictions"),
    )

    # Doctrine notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
        verbose_name=_("Notes"),
    )

    # Is doctrine active
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this doctrine is enabled or not"),
        verbose_name=_("Is enabled"),
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
        verbose_name=_("Name"),
    )

    # Formup location notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
        verbose_name=_("Notes"),
    )

    # Is formup location active?
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
        verbose_name=_("Is enabled"),
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
class DiscordPingTarget(models.Model):
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
        verbose_name=_("Group name"),
    )

    # Discord group id
    discord_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("ID of the Discord role to ping"),
        verbose_name=_("Discord ID"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="discord_role_require_groups",
        help_text=_("Restrict ping rights to the following groups …"),
        verbose_name=_("Group restrictions"),
    )

    # Notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
        verbose_name=_("Notes"),
    )

    # Is this group active?
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this formup location is enabled or not"),
        verbose_name=_("Is enabled"),
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
        verbose_name=_("Name"),
    )

    # Embed color
    embed_color = models.CharField(
        max_length=7,
        blank=True,
        help_text=_("Highlight color for the embed"),
        verbose_name=_("Embed color"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="fleettype_require_groups",
        help_text=_("Restrict this fleet type to the following groups …"),
        verbose_name=_("Group restrictions"),
    )

    # Fleet type notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this configuration here if you want"),
        verbose_name=_("Notes"),
    )

    # Is this fleet type enabled
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this fleet type is enabled or not"),
        verbose_name=_("Is enabled"),
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
        verbose_name=_("Discord channel"),
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
        verbose_name=_("Webhook URL"),
    )

    # Restrictions
    restricted_to_group = models.ManyToManyField(
        Group,
        blank=True,
        related_name="webhook_require_groups",
        help_text=_("Restrict ping rights to the following groups …"),
        verbose_name=_("Group restrictions"),
    )

    # Webhook notes
    notes = models.TextField(
        null=True,
        blank=True,
        help_text=_("You can add notes about this webhook here if you want"),
        verbose_name=_("Notes"),
    )

    # Is it enabled?
    is_enabled = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Whether this webhook is active or not"),
        verbose_name=_("Is enabled"),
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

        # Check if it's an actual Discord Webhook URL if the verification setting is set.
        if not re.match(
            DISCORD_WEBHOOK_REGEX, self.url
        ) and Setting.objects.get_setting(Setting.Field.WEBHOOK_VERIFICATION):
            raise ValidationError(
                _(
                    "Invalid webhook URL. The webhook URL you entered does not match "
                    "any known format for a Discord webhook. Please check the "
                    "webhook URL."
                )
            )

        super().clean()


class Setting(SingletonModel):
    """
    Default forum settings
    """

    class Field(models.TextChoices):
        """
        Choices for Setting.Field
        """

        USE_DEFAULT_FLEET_TYPES = "use_default_fleet_types", _(
            "Use default fleet types"
        )
        USE_DEFAULT_PING_TARGETS = "use_default_ping_targets", _(
            "Use default ping targets"
        )
        USE_DOCTRINES_FROM_FITTINGS_MODULE = "use_doctrines_from_fittings_module", _(
            "Use Doctrines from Fittings module"
        )
        WEBHOOK_VERIFICATION = "webhook_verification", _("Verify Webhooks")
        DEFAULT_EMBED_COLOR = "default_embed_color", _("Default embed color")

    use_default_fleet_types = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_(
            "Whether to use default fleet types. If checked, the default fleet types "
            "(Roaming, Home Defense, StratOP, and CTA) will be added to the Fleet Type "
            "dropdown."
        ),
        verbose_name=Field.USE_DEFAULT_FLEET_TYPES.label,
    )

    use_default_ping_targets = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_(
            "Whether to use default ping targets. If checked, the default ping targets "
            "(@everyone and @here) will be added to the Ping Target dropdown."
        ),
        verbose_name=Field.USE_DEFAULT_PING_TARGETS.label,
    )

    use_doctrines_from_fittings_module = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_(
            "Whether to use the doctrines from the Fittings modules in the doctrine "
            "dropdown. Note: The fittings module needs to be installed for this."
        ),
        verbose_name=Field.USE_DOCTRINES_FROM_FITTINGS_MODULE.label,
    )

    webhook_verification = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_(
            "Whether to verify Webhooks URLs or not. Note: When unchecked Webhook URLs "
            "will not be verified, so the app can be used with non-Discord Webhooks "
            "as well. When disabling webhook verification and using non-Discord "
            "webhooks, it is up to you to make sure your webhook understands a payload "
            "that is formatted for Discord webhooks."
        ),
        verbose_name=Field.WEBHOOK_VERIFICATION.label,
    )

    default_embed_color = models.CharField(
        default="#FAA61A",
        max_length=7,
        blank=True,
        help_text=_("Default highlight color for the webhook embed."),
        verbose_name=Field.DEFAULT_EMBED_COLOR.label,
    )

    objects = SettingManager()

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        default_permissions = ()
        verbose_name = _("setting")
        verbose_name_plural = _("settings")

    def __str__(self) -> str:
        return str(_("Fleet Pings Settings"))
